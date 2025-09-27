from django import views
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy


from main.business_logic.singleplayer_game import add_round, get_game_context
from main.models import Game


class GameView(views.View):
    def get(self, request, game_id: int):
        game = get_object_or_404(Game, pk=game_id)
        if request.user != game.player:
            return redirect(reverse_lazy("home"))
        return render(
            request, "single_player/game.html", context=get_game_context(game)
        )

    def post(self, request, game_id):
        points = int(request.POST.get("points", 0) or 0)
        game = get_object_or_404(Game, id=game_id)
        if request.user != game.player:
            return redirect(reverse_lazy("home"))
        game_status = add_round(game=game, points=points)
        if game_status == 1:
            return redirect(reverse_lazy("result", kwargs={"game_id": game.id}))
        if game_status == 2:
            return redirect(reverse_lazy("result", kwargs={"game_id": game.id}))
        return redirect(reverse_lazy("game", kwargs={"game_id": game.id}))
