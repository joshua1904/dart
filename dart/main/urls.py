from django.urls import path

from .views import StartGame, GameView, ResultView, StatisticsView

urlpatterns = [
    path('', StartGame.as_view(), name='home'),
    path('game/<int:game_id>/', GameView.as_view(), name='game'),
    path('results/<int:game_id>/', ResultView.as_view(), name='result'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]
