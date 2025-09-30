from main.constants import checkout_map


def get_points_of_round(left_score: int, points: int) -> int:
    if points > 180:
        points = 180
    if points < 0:
        points = 0

    if left_score - points < 0 or left_score - points == 1:
        points = 0
    if left_score == points and points not in checkout_map:
        points = 0
    return points


def get_checkout_suggestion(left_score: int) -> str | None:
    return checkout_map.get(left_score, None)
