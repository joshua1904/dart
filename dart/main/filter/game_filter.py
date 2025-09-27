import django_filters
from django import forms
from django.utils.functional import lazy
from main.models import Game


def get_rounds_choices():
    """Lazy function to get rounds choices from database"""
    try:
        return [
            (i, i)
            for i in Game.objects.values_list("rounds", flat=True).distinct()
            if i is not None
        ]
    except Exception:
        return []


def get_score_choices():
    """Lazy function to get score choices from database"""
    try:
        return [
            (i, i)
            for i in Game.objects.values_list("score", flat=True).distinct()
            if i is not None
        ]
    except Exception:
        return []


class GameFilter(django_filters.FilterSet):
    rounds = django_filters.ChoiceFilter(
        choices=lazy(get_rounds_choices, list)(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    score = django_filters.ChoiceFilter(
        choices=lazy(get_score_choices, list)(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={"class": "form-control", "type": "date"}
        )
    )

    class Meta:
        model = Game
        fields = ["rounds", "score", "date"]

    def filter_by_rounds(self, queryset, name, value):
        return queryset.filter(rounds=value)

    def filter_by_score(self, queryset, name, value):
        return queryset.filter(score=value)

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(date=value)

    def filter_by_status(self, queryset, name, value):
        return queryset.filter(status=value)
