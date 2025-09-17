from .single_player.start_game import StartGame
from .single_player.game import GameView
from .single_player.result import ResultView
from .statistics import StatisticsView
from .multiplayer.start_game import StartGame as MultiplayerStartGame
from .multiplayer.lobby import Lobby
__all__ = [
    StartGame.__name__,
    GameView.__name__,
    ResultView.__name__,
    MultiplayerStartGame.__name__,
    Lobby.__name__,
]

