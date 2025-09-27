from django import views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from main.forms.game_form import GameForm


class StartGame(views.View):
    def get(self, request):
        form = GameForm(initial={"rounds": 3, "score": 121})
        return render(
            request,
            "single_player/start_game.html",
            context={"rounds": 3, "score": 121, "form": form},
        )

    def post(self, request):
        form = GameForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "single_player/start_game.html",
                context={"rounds": 3, "score": 121, "form": form},
            )

        game = form.save(commit=False)
        game.player = request.user
        game.save()
        return redirect(reverse_lazy("game", kwargs={"game_id": game.id}))
