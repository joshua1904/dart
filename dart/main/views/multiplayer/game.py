from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from main.models import MultiplayerGame
from main.business_logic.multiplayer_game import get_game_context, get_ending_context
from main.utils import MultiplayerGameStatus


class MultiplayerGameView(views.View):
    def get(self, request, game_id):
        game = get_object_or_404(MultiplayerGame, id=game_id)
        user = request.user
        # If game not started, send back to lobby
        if game.status == MultiplayerGameStatus.WAITING.value:
            messages.info(request, "Game has not started yet.")
            return redirect(reverse_lazy("lobby", kwargs={"game_id": game.id}))
        if game.status == MultiplayerGameStatus.FINISHED.value:
            context = get_ending_context(game)
            return render(
                request, "multiplayer/game/partials/ending_screen.html", context=context
            )
        if not game.online and not user == game.creator:
            messages.info(request, "Game is not online!")
            return redirect(reverse_lazy("lobby", kwargs={"game_id": game.id}))
        if not request.user not in game.game_players.all():
            messages.info(request, "You are not part of this game!")
            return redirect(reverse_lazy("lobby", kwargs={"game_id": game.id}))
        context = get_game_context(game)
        return render(request, "multiplayer/game/game.html", context=context)
