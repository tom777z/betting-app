from django.forms import ModelForm
from .models import Game, Bet
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = 'home_team', 'away_team', 'league', 'date', 'home_goals', 'away_goals', 'round', 

        widgets = {
            'date': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            'active': forms.CheckboxSelectMultiple()  
        }

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data.get('home_team')
        away_team = cleaned_data.get('away_team')
        
        if home_team == away_team:
            raise ValidationError(
                'Home team and Away team can\'t have the same value')
    
class UpdateGameForm(ModelForm):
    class Meta:
        model = Game
        fields = 'home_team', 'away_team', 'league', 'date', 'home_goals', 'away_goals', 'round', 'active'

        widgets = {
            'date': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),    
        }

    def __init__(self, *args, **kwargs):
        super(UpdateGameForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data.get('home_team')
        away_team = cleaned_data.get('away_team')
        if home_team == away_team:
            raise ValidationError(
                'Home team and Away team can\'t have the same value')

        return cleaned_data
    
class BetForm(ModelForm):
    class Meta:
        model = Bet
        fields = 'game', 'home_goals', 'away_goals'

    def __init__(self, *args, **kwargs):
        super(BetForm, self).__init__(*args, **kwargs)
        self.fields['game'].queryset = Game.objects.filter(date__gt=timezone.now()).filter(active=True)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    
class UpdateBetForm(ModelForm):
    class Meta:
        model = Bet
        fields = 'player', 'game', 'home_goals', 'away_goals'

    def __init__(self, *args, **kwargs):
        super(UpdateBetForm, self).__init__(*args, **kwargs)
        self.fields['game'].queryset = Game.objects.filter(date__gt=timezone.now()).filter(active=True)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})