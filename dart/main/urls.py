from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import StartGame, GameView, ResultView, StatisticsView, MultiplayerStartGame, Lobby

single_player_urlpatterns = [
    path('', login_required(StartGame.as_view()), name='home'),
    path('game/<int:game_id>/', login_required(GameView.as_view()), name='game'),
    path('results/<int:game_id>/', login_required(ResultView.as_view()), name='result'),
    path('statistics/', login_required(StatisticsView.as_view()), name='statistics'),
]

multiplayer_urlpatterns = [
    path('multiplayer/', login_required(MultiplayerStartGame.as_view()), name='multiplayer_home'),
    path('multiplayer/lobby/<uuid:game_id>/', login_required(Lobby.as_view()), name='lobby'),
]

urlpatterns = single_player_urlpatterns + multiplayer_urlpatterns