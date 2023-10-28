from django.contrib import admin
from .models import Game, Team, League, Country, Player, Bet, Round

class BetAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "game", "home_goals", "away_goals", "result", "score"]
    list_display_links = ("player", "game")

class BetInline(admin.TabularInline):
    model = Bet

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "home_team", "away_team", "league", "date"]
    inlines=[BetInline]

admin.site.register(Team)
admin.site.register(League)
admin.site.register(Country)
admin.site.register(Player)
admin.site.register(Bet, BetAdmin)
admin.site.register(Round)
