from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    HomeView,
    StartGame,
    GameView,
    ResultView,
    StatisticsView,
    MultiplayerStartGame,
    Lobby,
    MultiplayerGameView,
    MultiplayerGameOverviewView,
)

home_urlpatterns = [
    path("", login_required(HomeView.as_view()), name="home"),
]

single_player_urlpatterns = [
    path("singleplayer/", login_required(StartGame.as_view()), name="singleplayer"),
    path(
        "singleplayer/game/<uuid:game_id>/",
        login_required(GameView.as_view()),
        name="game",
    ),
    path(
        "singleplayer/results/<uuid:game_id>/",
        login_required(ResultView.as_view()),
        name="result",
    ),
    path(
        "singleplayer/statistics/",
        login_required(StatisticsView.as_view()),
        name="statistics",
    ),
]

multiplayer_urlpatterns = [
    path(
        "multiplayer/",
        login_required(MultiplayerStartGame.as_view()),
        name="multiplayer",
    ),
    path(
        "multiplayer/lobby/<uuid:game_id>/",
        login_required(Lobby.as_view()),
        name="lobby",
    ),
    path(
        "multiplayer/game/<uuid:game_id>/",
        login_required(MultiplayerGameView.as_view()),
        name="multiplayer_game",
    ),
    path(
        "multiplayer/game/<uuid:game_id>/overview/",
        login_required(MultiplayerGameOverviewView.as_view()),
        name="multiplayer_game_overview",
    ),
]

urlpatterns = home_urlpatterns + single_player_urlpatterns + multiplayer_urlpatterns
