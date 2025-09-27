from django import forms

from main.models import MultiplayerGame


class MultiplayerGameForm(forms.ModelForm):
    max_players = forms.IntegerField(
        label="Players",
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter max players",
            }
        ),
    )
    online = forms.BooleanField(
        label="Online",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "default": False,
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
        model = MultiplayerGame
        fields = ("max_players", "online", "score")
