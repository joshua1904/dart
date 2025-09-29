from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg

from main.business_logic.utils import get_points_of_round, get_checkout_suggestion
from main.models import MultiplayerGame, MultiplayerPlayer, MultiplayerRound
from main.utils import GameStatus


def get_game_info(game_id: int):
    game = get_object_or_404(MultiplayerGame, id=game_id)
    return game


def get_turn(game) -> int:
    last_turn = game.game_rounds.order_by("id").last()
    # if no rounds, return 1
    if not last_turn or game.max_players == 1:
        return 1
    last_rank = last_turn.player.rank
    if last_rank == game.max_players:
        return 1
    return last_rank + 1


def get_left_score(game, game_player) -> int:
    total_points = game.game_rounds.filter(player=game_player).aggregate(
        total_points=Sum("points")
    )["total_points"]
    # If no rounds exist, total_points will be None, so default to 0
    if total_points is None:
        total_points = 0
    return game.score - total_points


def get_queue(game, turn: int) -> list:
    queue = list(game.game_players.order_by("rank").values_list("rank", flat=True))
    return queue[turn:] + queue[: turn - 1]


def get_game_context(game) -> dict:
    current_user = get_object_or_404(MultiplayerPlayer, game=game, rank=get_turn(game))
    queue_list = []
    for rank in get_queue(game, current_user.rank):
        player = game.game_players.get(rank=rank)
        queue_list.append(
            {
                "player": player,
                "left_score": get_left_score(game, player),
                "checkout_suggestion": get_checkout_suggestion(
                    get_left_score(game, player)
                ),
            }
        )
    return {
        "game": game,
        "turn": current_user,
        "left_score": get_left_score(game, current_user),
        "checkout_suggestion": get_checkout_suggestion(
            get_left_score(game, current_user)
        ),
        "queue": queue_list,
    }


def add_round(game, player, points) -> bool:
    left_score = get_left_score(game, player)
    points = get_points_of_round(left_score, points)
    MultiplayerRound(game=game, player=player, points=points).save()
    if left_score == points:
        game.status = GameStatus.WON.value
        game.winner = player
        game.save()
        return True
    return False


def get_average_points(game, player) -> float:
    return game.game_rounds.filter(player=player).aggregate(
        average_points=Avg("points")
    )["average_points"]


def get_needed_rounds(game, player) -> int:
    return game.game_rounds.filter(player=player).count()


def get_ending_context(game) -> dict:
    winner_stats = {
        "average_points": get_average_points(game, game.winner),
        "needed_rounds": get_needed_rounds(game, game.winner),
    }
    return {
        "game": game,
        "winner": game.winner,
        "winner_stats": winner_stats,
    }
