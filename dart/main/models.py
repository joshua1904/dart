from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Game(models.Model):
    date = models.DateField(default=timezone.now())
    rounds = models.IntegerField(validators=[MinValueValidator(0)])
    score = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.IntegerField(
        choices=((0, 'in progress'), (1, 'won'), (2, 'lost')),
        default=0
    )


class Round(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_rounds')
    points = models.IntegerField( validators=[MaxValueValidator(180), MinValueValidator(0)])



