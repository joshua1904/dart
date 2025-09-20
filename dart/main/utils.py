
import enum

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
