from dataclasses import dataclass

from main.models import Game


@dataclass
class Statistics:
    wins: int = 0
    losses: int = 0
    total_games: int = 0
    total_points: int = 0

    @property
    def win_rate(self) -> float:
        return self.wins / self.total_games

    @property
    def loss_rate(self) -> float:
        return self.losses / self.total_games

    @property
    def average_points(self) -> float:
        return self.total_points / self.total_games


def get_statistics(games: list[Game]) -> Statistics:
    pass
