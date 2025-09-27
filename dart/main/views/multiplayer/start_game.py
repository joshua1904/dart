from django import views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from main.forms.multiplayer_game_form import MultiplayerGameForm


class StartGame(views.View):
    def get(self, request):
        form = MultiplayerGameForm(
            initial={"max_players": 2, "online": False, "score": 301}
        )
        return render(request, "multiplayer/start_game.html", context={"form": form})

    def post(self, request):
        form = MultiplayerGameForm(request.POST)
        if not form.is_valid():
            return render(
                request, "multiplayer/start_game.html", context={"form": form}
            )

        game = form.save(commit=False)
        game.creator = request.user
        game.save()
        # Add the creator as the first player
        from main.models import MultiplayerPlayer

        MultiplayerPlayer.objects.create(
            game=game,
            player=request.user,
            rank=1,
        )
        return redirect(reverse_lazy("lobby", kwargs={"game_id": game.id}))
