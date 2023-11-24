from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_save
from signals import *
from django.urls import reverse 


def replace_polish_chars(text):
    polish_chars='ĄąĆćĘęŁłŃńÓóŚśŹźŻż'
    replacements='AaCcEeLlNnOoSsZzZz'
    t = str.maketrans(polish_chars,replacements)
    return text.translate(t)

def calculate_result(home,away):
    if home != None and away != None:
        if home == away:
            return 'D'
        elif home > away:
            return 'H'
        elif home < away: 
            return 'A'

class Game(models.Model):
    
    RESULTS = [
        ("H", "Home"),
        ("A", "Away"),
        ("D", "Draw"),
    ]

    home_team = models.ForeignKey("Team", on_delete=models.RESTRICT, related_name='home_team')
    away_team = models.ForeignKey("Team", on_delete=models.RESTRICT, related_name='away_team')
    league = models.ForeignKey("League", on_delete=models.RESTRICT, )
    home_goals = models.PositiveSmallIntegerField(blank=True, null=True)
    away_goals = models.PositiveSmallIntegerField(blank=True, null=True)
    result = models.CharField(max_length=1, choices=RESULTS,blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(null=True)
    active = models.BooleanField(blank=True, default=True)
    round = models.ForeignKey("Round", on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.home_team} - {self.away_team} on {self.date}"

    def save(self, *args, **kwargs):
        slg = f"{replace_polish_chars(str(self.home_team))}-{replace_polish_chars(str(self.away_team))}-{self.date.strftime('%Y-%m-%d')}-{str(timezone.now())}"
        self.slug = slugify(slg)
        self.result = calculate_result(self.home_goals, self.away_goals) 

        super().save(*args, **kwargs)

    def clean(self):
        if self.round is None:
            raise ValidationError('Round is mandatory')
    
class Team(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey("Country", on_delete=models.RESTRICT)
    
    def __str__(self):
        return self.name
    
class League(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey("Country", on_delete=models.RESTRICT)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    nickname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(null=True, upload_to='profiles/', default="profiles/default.png")
    
    def __str__(self):
        return self.nickname
    
class Bet(models.Model):
    
    RESULTS = [
        ("H", "Home"),
        ("A", "Away"),
        ("D", "Draw"),
    ]

    player = models.ForeignKey("Player", on_delete=models.RESTRICT)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    home_goals = models.PositiveSmallIntegerField()
    away_goals = models.PositiveSmallIntegerField()
    result = models.CharField(max_length=1, choices=RESULTS, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.home_goals} : {self.away_goals}"
    
    def get_absolute_url(self):
        return reverse('bet', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.result = calculate_result(self.home_goals, self.away_goals)
        dup = Bet.objects.filter(player_id=self.player).filter(game=self.game)
        if dup.exists() == True: #avoid bet duplicates
            return
        
        super().save(*args, **kwargs)


class Round(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name