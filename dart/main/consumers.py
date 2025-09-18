import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from main.models import MultiplayerGame, MultiplayerPlayer, MultiplayerRound
from django.template.loader import render_to_string
from urllib.parse import parse_qs
from main.business_logic.multiplayer_game import get_game_context, get_turn, add_round


class MultiplayerConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game = MultiplayerGame.objects.get(id=self.game_id)
        async_to_sync(self.channel_layer.group_add)(str(self.game_id), self.channel_name)
        self.accept()
    

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(str(self.game_id), self.channel_name)

    def receive(self, text_data):
        
        data = {}
        # Try JSON first (manual sends), then fallback to form-encoded (htmx ws-send)
        try:
            data = json.loads(text_data)
        except Exception:
            try:
                parsed = {k: v[0] if isinstance(v, list) and v else v for k, v in parse_qs(text_data).items()}
                data.update(parsed)
            except Exception:
                pass
        # Ensure sender is tracked as player
        if not MultiplayerPlayer.objects.filter(game=self.game, player=self.user).exists():
            MultiplayerPlayer.objects.create(
                game=self.game,
                player=self.user,
                rank=self.game.game_players.count() + 1
            )

        # Handle actions
        action = data.get('action')
        if action == 'start_game':
            # Only host can start
            if self.user == self.game.creator:
                # Mark game as started
                self.game.status = 1
                self.game.save(update_fields=['status'])
                # Broadcast redirect to all clients in group
                async_to_sync(self.channel_layer.group_send)(
                    str(self.game_id),
                    {
                        'type': 'redirect_all',
                        'url': f"/multiplayer/game/{self.game_id}/"
                    }
                )
            return

        # Default: update lobby content
        event = {
            'type': 'send_lobby_content',
            'game_id': self.game_id
        }
        async_to_sync(self.channel_layer.group_send)(str(self.game_id), event)
    
    def send_lobby_content(self, event):
        game_id = event['game_id']
        game = MultiplayerGame.objects.get(id=game_id)
        
        html = render_to_string('multiplayer/lobby/partials/player_list.html', context={'game': game, 'players': game.game_players.all(), 'user': self.user})
        self.send(text_data=f'<div id="lobby-content" hx-swap-oob="innerHTML">{html}</div>')

    def redirect_all(self, event):
        print(event)
        url = event['url']
        # Send JSON message with redirect instruction
        redirect_message = {
            'type': 'redirect',
            'url': url
        }
        self.send(text_data=json.dumps(redirect_message))

class GameConsumer(WebsocketConsumer):
    def connect(self):
        print("GameConsumer connected")
        self.user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game = MultiplayerGame.objects.get(id=self.game_id)
        async_to_sync(self.channel_layer.group_add)(str(self.game_id), self.channel_name)
        self.accept()
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(str(self.game_id), self.channel_name)

    def receive(self, text_data):
        print("GameConsumer received:", text_data)
        
        data = {}
        # Try JSON first (manual sends)
        try:
            data = json.loads(text_data)
        except Exception:
            # Fallback to form-encoded (htmx ws-send)
            try:
                parsed = {k: v[0] if isinstance(v, list) and v else v for k, v in parse_qs(text_data).items()}
                data.update(parsed)
            except Exception:
                pass

        points = data.get('points')
        if not points:
            points = 0
        print(f"Adding {points} points for turn {get_turn(self.game)}")
        player = self.game.game_players.get(rank=get_turn(self.game))
        if player.player != self.scope['user']:
            return
        if add_round(self.game, player, int(points)):
            event = {
                'type': 'game_ended',
                'game_id': self.game_id
            }
            async_to_sync(self.channel_layer.group_send)(str(self.game_id), event)
            return
            
        # Update game content
        event = {
            'type': 'send_game_content',
            'game_id': self.game_id
        }
        async_to_sync(self.channel_layer.group_send)(str(self.game_id), event)
    
    def send_game_content(self, event):
        game_id = event['game_id']
        game = MultiplayerGame.objects.get(id=game_id)
        context = get_game_context(game)
        context['user'] = self.scope['user']
        html = render_to_string('multiplayer/game/partials/game_card.html', context=context)
        self.send(text_data=f'<div id="game-content" hx-swap-oob="innerHTML">{html}</div>')

    def game_ended(self, event):
        game_id = event['game_id']
        print("Game ended")
        game = MultiplayerGame.objects.get(id=game_id)
        context = get_game_context(game)
        context['winner'] = game.winner
        html = render_to_string('multiplayer/game/partials/ending_screen.html', context=context)
        self.send(text_data=f'<div id="game-content" hx-swap-oob="innerHTML">{html}</div>')