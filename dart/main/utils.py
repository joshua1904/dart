import enum
import random
from copy import copy

from .constants import first_names, last_names


class MultiplayerGameStatus(enum.Enum):
    WAITING = 0
    PROGRESS = 1
    FINISHED = 2


class GameStatus(enum.Enum):
    PROGRESS = 0
    WON = 1
    LOST = 2


GAME_STATUS_CHOICES = [
    (GameStatus.PROGRESS.value, GameStatus.PROGRESS.name),
    (GameStatus.WON.value, GameStatus.WON.name),
    (GameStatus.LOST.value, GameStatus.LOST.name),
]

MULTIPLAYER_GAME_STATUS_CHOICES = [
    (MultiplayerGameStatus.WAITING.value, MultiplayerGameStatus.WAITING.name),
    (MultiplayerGameStatus.PROGRESS.value, MultiplayerGameStatus.PROGRESS.name),
    (MultiplayerGameStatus.FINISHED.value, MultiplayerGameStatus.FINISHED.name),
]


def get_random_name(names: list):
    return random.choice(names)


def get_random_names(names: list, count: int) -> list:
    names = copy(names)
    random.shuffle(names)
    return names


def get_guest_names(guest_count: int) -> list:
    guest_first_names = get_random_names(first_names, guest_count)
    guest_last_names = get_random_names(last_names, guest_count)

    return [
        f"{first_name} {last_name}"
        for first_name, last_name in zip(guest_first_names, guest_last_names)
    ]
