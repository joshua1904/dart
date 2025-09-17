from django import views
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from main.models import Game, Round


def get_game_info(game_id: int):
    game = get_object_or_404(Game, id=game_id)
    rounds = Round.objects.filter(game=game)
    round_count = rounds.count()
    current_score_left = game.score - sum(rounds.values_list('points', flat=True))
    return game, rounds, round_count, current_score_left


class GameView(views.View):

    def get(self, request, game_id: int):
        game, _, round_count, current_score_left = get_game_info(game_id)
        return render(request, 'game.html', context={'round_count': round_count, 'current_score_left': current_score_left, 'game': game})

    def post(self, request, game_id):
        game, _, round_count, current_score_left = get_game_info(game_id)
        points = int(request.POST.get('this_score', 0))
        left_score = current_score_left - points
        if left_score <= 1 and left_score != 0:
            points = 0
        Round(game=game, points=points).save()
        if left_score == 0:
            game.status = 1
            game.save()
            return redirect(reverse_lazy('result', kwargs={'game_id': game.id}))

        if round_count + 1 == game.rounds:
            game.status = 2
            game.save()
            return redirect(reverse_lazy('result', kwargs={'game_id': game.id}))


        return redirect(reverse_lazy('game', kwargs={'game_id': game.id}))


