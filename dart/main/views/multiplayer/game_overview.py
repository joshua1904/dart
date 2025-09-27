from django import views
from django.shortcuts import get_object_or_404, render
from main.models import MultiplayerGame
from main.business_logic.multiplayer_game import get_ending_context


class MultiplayerGameOverviewView(views.View):
    def get(self, request, game_id: int):
        game = get_object_or_404(MultiplayerGame, id=game_id)
        context = get_ending_context(game)
        return render(request, "multiplayer/game/overview.html", context=context)
