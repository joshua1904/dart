from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from main.models import MultiplayerGame, MultiplayerPlayer
from main.utils import MULTIPLAYER_GAME_STATUS_CHOICES, MultiplayerGameStatus


# Lobby for multiplayer game
class Lobby(views.View):
    def get(self, request, game_id):
        game = get_object_or_404(MultiplayerGame, id=game_id)
        players = game.game_players.all()
        current_user = request.user
        current_user_in_game = players.filter(player=current_user).exists()
        if (
            game.status != MultiplayerGameStatus.WAITING.value
            or (not game.online and not current_user == game.creator)
            or (
                game.max_players <= game.game_players.count()
                and not current_user_in_game
            )
        ):
            messages.error(
                request,
                "Game is not in waiting status or is not online or has reached the maximum number of players",
            )
            return redirect(reverse_lazy("home"))

        return render(
            request,
            "multiplayer/lobby/lobby.html",
            context={
                "game": game,
                "players": players,
                "current_user_in_game": current_user_in_game,
            },
        )
