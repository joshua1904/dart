from django import views
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from main.models import Game
from main.utils import GameStatus


class ResultView(views.View):
    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        rounds = game.game_rounds.all()

        total_points = sum(rounds.values_list("points", flat=True))
        round_count = rounds.count()
        score_difference = game.score - total_points

        games_today = Game.objects.filter(
            date=timezone.now(), rounds=game.rounds, score=game.score
        ).order_by("-id")
        last_5 = len(games_today[:5])
        last_5_won = sum(
            1 for game in games_today[:5] if game.status == GameStatus.WON.value
        )
        games_today_won = games_today.filter(status=GameStatus.WON.value).count()
        games_today_lost = games_today.filter(status=GameStatus.LOST.value).count()

        return render(
            request,
            "single_player/result.html",
            context={
                "game": game,
                "total_points": total_points,
                "round_count": round_count,
                "score_difference": score_difference,
                "games_today_won": games_today_won,
                "games_today_lost": games_today_lost,
                "last_5_won": last_5_won,
                "last_5": last_5,
                "percentage": last_5_won / last_5 * 100,
                "category": f"{game.rounds} darts for {game.score} points",
            },
        )

    def post(self, request, game_id):
        """create new game with same stats"""
        last_game = get_object_or_404(Game, id=game_id)
        new_game = Game(
            rounds=last_game.rounds, score=last_game.score, player=last_game.player
        )
        new_game.save()
        return redirect(reverse_lazy("game", kwargs={"game_id": new_game.id}))
