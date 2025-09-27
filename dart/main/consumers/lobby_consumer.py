import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from main.models import MultiplayerGame, MultiplayerPlayer
from django.template.loader import render_to_string
from urllib.parse import parse_qs
from main.utils import MultiplayerGameStatus, get_guest_names


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]

        # Check if user is authenticated
        if not self.user.is_authenticated:
            self.close()
            return

        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game = MultiplayerGame.objects.get(id=self.game_id)
        async_to_sync(self.channel_layer.group_add)(
            str(self.game_id), self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            str(self.game_id), self.channel_name
        )

    def receive(self, text_data):

        data = {}
        # Try JSON first (manual sends), then fallback to form-encoded (htmx ws-send)
        try:
            data = json.loads(text_data)
        except Exception:
            try:
                parsed = {
                    k: v[0] if isinstance(v, list) and v else v
                    for k, v in parse_qs(text_data).items()
                }
                data.update(parsed)
            except Exception:
                pass
        # Ensure sender is tracked as player
        if not MultiplayerPlayer.objects.filter(
            game=self.game, player=self.user
        ).exists():
            MultiplayerPlayer.objects.create(
                game=self.game,
                player=self.user,
                rank=self.game.game_players.count() + 1,
            )

        # Handle actions
        action = data.get("action")
        if action == "start_game":
            # Only host can start
            if self.user == self.game.creator:
                # Mark game as started
                self.game.status = MultiplayerGameStatus.PROGRESS.value
                self.game.save(update_fields=["status"])
                missing_players = self.game.max_players - self.game.game_players.count()
                guest_names = get_guest_names(missing_players)
                current_player_count = self.game.game_players.count()
                for counter in range(missing_players):
                    MultiplayerPlayer.objects.create(
                        game=self.game,
                        player=None,
                        rank=current_player_count + counter + 1,
                        guest_name=guest_names[counter],
                    )
                # Broadcast redirect to all clients in group
                async_to_sync(self.channel_layer.group_send)(
                    str(self.game_id),
                    {
                        "type": "redirect_all",
                        "url": f"/multiplayer/game/{self.game_id}/",
                    },
                )
            return

        # Default: update lobby content
        event = {"type": "send_lobby_content", "game_id": self.game_id}
        async_to_sync(self.channel_layer.group_send)(str(self.game_id), event)

    def send_lobby_content(self, event):
        game_id = event["game_id"]
        game = MultiplayerGame.objects.get(id=game_id)

        html = render_to_string(
            "multiplayer/lobby/partials/player_list.html",
            context={
                "game": game,
                "players": game.game_players.all(),
                "user": self.user,
            },
        )
        self.send(
            text_data=f'<div id="lobby-content" hx-swap-oob="innerHTML">{html}</div>'
        )

    def redirect_all(self, event):
        url = event["url"]
        # Send JSON message with redirect instruction
        redirect_message = {"type": "redirect", "url": url}
        self.send(text_data=json.dumps(redirect_message))
