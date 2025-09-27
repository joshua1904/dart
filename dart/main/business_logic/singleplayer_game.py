from django.db.models import Sum

from main.business_logic.utils import get_points_of_round, get_checkout_suggestion
from main.models import Round, Game
from main.utils import GameStatus


def get_game_context(game: Game) -> dict:
    rounds = Round.objects.filter(game=game)
    round_count = rounds.count()
    current_score_left = game.score - sum(rounds.values_list("points", flat=True))
    checkout_suggestion = get_checkout_suggestion(current_score_left)
    total_points_scored = sum(rounds.values_list("points", flat=True))
    average_score = (
        round(total_points_scored / round_count, 1) if round_count > 0 else 0
    )
    return {
        "game": game,
        "rounds": rounds,
        "round_count": round_count,
        "current_score_left": current_score_left,
        "checkout_suggestion": checkout_suggestion,
        "average_score": average_score,
        "total_points_scored": total_points_scored,
    }


def get_left_points(game: Game) -> int:
    total_points = (
        game.game_rounds.all().aggregate(total_points=Sum("points"))["total_points"]
        or 0
    )
    return game.score - total_points


def add_round(game: Game, points: int):
    left_points = get_left_points(game)
    points = get_points_of_round(left_points, points)
    Round(game=game, points=points).save()
    left_points -= points
    if left_points == 0:
        game.status = GameStatus.WON.value
        game.save()
        return game.status
    if game.game_rounds.count() == game.rounds:
        game.status = GameStatus.LOST.value
        game.save()
    return game.status
