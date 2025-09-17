from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from main.models import MultiplayerGame, MultiplayerPlayer
from main.utils import MULTIPLAYER_GAME_STATUS_CHOICES

# Lobby for multiplayer game
class Lobby(views.View):
    def get(self, request, game_id):
        game = get_object_or_404(MultiplayerGame, id=game_id)
        players = game.game_players.all()

        current_user = request.user
        current_user_in_game = players.filter(player=current_user).exists()

        if current_user_in_game:
            return render(request, 'multiplayer/lobby.html', context={'game_id': game_id, 'players': players})

        if game.status != 0 or not game.online or game.max_players <= game.game_players.count():
            messages.error(request, 'Game is not in waiting status or is not online or has reached the maximum number of players')
            return redirect(reverse_lazy('home'))
        MultiplayerPlayer.objects.create(game=game, player=request.user, rank=players.count() + 1)
        return render(request, 'multiplayer/lobby.html', context={'game_id': game_id, 'players': players})