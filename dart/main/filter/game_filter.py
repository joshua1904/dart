import django_filters
from django.db.models import Q
from django import forms
from main.models import Game
from main.utils import GAME_STATUS_CHOICES
from django.urls import reverse_lazy

class GameFilter(django_filters.FilterSet):
    rounds = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Game.objects.values_list('rounds', flat=True).distinct()],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    score = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Game.objects.values_list('score', flat=True).distinct()],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control', 'type': 'date'})
    )
    class Meta:
        model = Game
        fields = ['rounds', 'score', 'date']    

    def filter_by_rounds(self, queryset, name, value):
        return queryset.filter(rounds=value)
    
    def filter_by_score(self, queryset, name, value):
        return queryset.filter(score=value)
    
    def filter_by_date(self, queryset, name, value):
        return queryset.filter(date=value)
    
    def filter_by_status(self, queryset, name, value):
        return queryset.filter(status=value)