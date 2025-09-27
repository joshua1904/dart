from django.contrib import admin
from .models import Game, Round, MultiplayerGame, MultiplayerRound, MultiplayerPlayer

# Register your models here.


admin.site.register(Game)


admin.site.register(Round)

admin.site.register(MultiplayerGame)
admin.site.register(MultiplayerRound)
admin.site.register(MultiplayerPlayer)
