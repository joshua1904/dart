from django import views
from django.shortcuts import render
from main.models import Game
from main.filter.game_filter import GameFilter


class StatisticsView(views.View):
    def get(self, request):
        scores = Game.objects.values_list("score", flat=True).distinct()
        rounds = Game.objects.values_list("rounds", flat=True).distinct()
        games = Game.objects.all()
        filter = GameFilter(request.GET, queryset=games)
        games = filter.qs
        if request.META.get("HTTP_HX_REQUEST"):
            return render(
                request,
                "statistics.detail.html",
                context={
                    "games": games,
                    "filter": filter,
                    "scores": scores,
                    "rounds": rounds,
                },
            )

        return render(
            request,
            "statistics.html",
            context={
                "games": games,
                "filter": filter,
                "scores": scores,
                "rounds": rounds,
            },
        )
