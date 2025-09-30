import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from main.models import MultiplayerGame, MultiplayerPlayer
from django.template.loader import render_to_string
from urllib.parse import parse_qs
from main.business_logic.multiplayer_game import get_game_context, get_turn, add_round
import logging

logger = logging.getLogger(__name__)


class GameConsumer(WebsocketConsumer):
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

    def new_game(self):
        new_game = MultiplayerGame(
            score=self.game.score,
            creator=self.user,
            max_players=self.game.max_players,
            online=self.game.online,
            status=1,
        )
        new_game.save()
        for player in self.game.game_players.all():
            MultiplayerPlayer.objects.create(
                game=new_game,
                player=player.player,
                rank=player.rank,
                guest_name=player.guest_name,
            )
        logger.info(f"New game created: {new_game.id}")
        event = {"type": "redirect_all", "url": f"/multiplayer/game/{new_game.id}/"}
        # Send redirect to current game group (where clients are connected)
        async_to_sync(self.channel_layer.group_send)(str(self.game_id), event)

    def receive(self, text_data):

        data = {}
        # Try JSON first (manual sends)
        try:
            data = json.loads(text_data)
        except Exception:
            # Fallback to form-encoded (htmx ws-send)
            try:
                parsed = {
                    k: v[0] if isinstance(v, list) and v else v
                    for k, v in parse_qs(text_data).items()
                }
                data.update(parsed)
            except Exception:
                pass
        if data.get("action") == "new_game":
            self.new_game()
            return
        points = data.get("points")
        if not points:
            points = 0
        player = self.game.game_players.get(rank=get_turn(self.game))
        if player.player != self.scope["user"] and player.player != None:
            logger.warning(f"Player {player.player} is not the current player")
            return
        # add round returns true if game is ended
        if add_round(self.game, player, int(points)):
            event = {
                "type": "redirect_all",
                "url": f"/multiplayer/game/{self.game_id}/overview/",
            }
            async_to_sync(self.channel_layer.group_send)(str(self.game_id), event)
            return

        # Update game content
        event = {"type": "send_game_content", "game_id": self.game_id}
        async_to_sync(self.channel_layer.group_send)(str(self.game_id), event)

    def send_game_content(self, event):
        game_id = event["game_id"]
        game = MultiplayerGame.objects.get(id=game_id)
        context = get_game_context(game)
        context["user"] = self.scope["user"]
        html = render_to_string(
            "multiplayer/game/partials/game_card.html", context=context
        )
        self.send(
            text_data=f'<div id="game-content" hx-swap-oob="innerHTML">{html}</div>'
        )

    def redirect_all(self, event):
        url = event["url"]
        # Send JSON message with redirect instruction
        redirect_message = {"type": "redirect", "url": url}
        self.send(text_data=json.dumps(redirect_message))
