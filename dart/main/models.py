from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from main.utils import GAME_STATUS_CHOICES, MULTIPLAYER_GAME_STATUS_CHOICES
import uuid


# single player
class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=timezone.now)
    rounds = models.IntegerField(validators=[MinValueValidator(0)])
    score = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.IntegerField(choices=GAME_STATUS_CHOICES, default=0)
    player = ForeignKey("auth.User", on_delete=models.CASCADE)


class Round(models.Model):
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="game_rounds"
    )
    points = models.IntegerField(
        validators=[MaxValueValidator(180), MinValueValidator(0)]
    )


# multiplayer
class MultiplayerGame(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=timezone.now)
    score = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.IntegerField(choices=MULTIPLAYER_GAME_STATUS_CHOICES, default=0)
    online = models.BooleanField(default=False)
    max_players = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    winner = models.ForeignKey(
        "MultiplayerPlayer",
        on_delete=models.CASCADE,
        related_name="winner",
        null=True,
        blank=True,
    )


class MultiplayerRound(models.Model):
    game = models.ForeignKey(
        "MultiplayerGame", on_delete=models.CASCADE, related_name="game_rounds"
    )
    points = models.IntegerField(
        validators=[MaxValueValidator(180), MinValueValidator(0)]
    )
    player = models.ForeignKey(
        "MultiplayerPlayer", on_delete=models.CASCADE, related_name="player_rounds"
    )


class MultiplayerPlayer(models.Model):
    game = models.ForeignKey(
        "MultiplayerGame", on_delete=models.CASCADE, related_name="game_players"
    )
    player = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True
    )
    rank = models.IntegerField()
    guest_name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.player.username if self.player else self.guest_name or ""

    @property
    def display_name(self):
        return self.player.username if self.player else self.guest_name or ""
