from django import forms

from main.models import Game


class GameForm(forms.ModelForm):
    rounds = forms.IntegerField(
        label="Max Rounds",
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter max rounds",
            }
        ),
    )

    score = forms.IntegerField(
        label="Score",
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Starting score",
            }
        ),
    )

    class Meta:
        model = Game
        fields = ("score", "rounds")
