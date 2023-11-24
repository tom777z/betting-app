from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Game, Bet, Player, Round
from .forms import GameForm, BetForm, UpdateGameForm, ProfileUpdateForm
from django.utils import timezone
from datetime import datetime
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Coalesce
from operator import itemgetter
from django.contrib import messages
import csv
from django.http import HttpResponse

def calculate_score(b_hg, b_ag, b_r, g_hg, g_ag, g_r):
    points = 0

    if b_hg == g_hg and b_ag == g_ag:
        points = 3
    elif b_r == g_r:
        points = 1
   
    return points

class indexView(ListView):
    model = Game
    context_object_name = 'games'
    template_name = 'betting_app/index.html'

    paginate_by = 6  
    
    def get_queryset(self):
        
        #default query
        queryset = Game.objects.values("id", "slug", "date", "league__name", 
                            "home_team__id", "home_team__name", "away_team__name", "round__name").filter(date__gt=timezone.now()).filter(active=True).order_by("date")

        pcount = Player.objects.count()
     
        if pcount > 0:
            player_id = None
            user_id = self.request.user.id #logged user id
            if user_id:
                player = Player.objects.select_related("user").values("id").filter(user_id=user_id).get() #get player based on logged user id
                player_id = int(player['id'])
            
                if player_id is not None:
                    queryset = Game.objects.filter(date__gt=timezone.now()).filter(active=True).order_by("date").values("id", "slug", "date", "league__name", 
                                "home_team__id", "home_team__name", "away_team__name", "round__name").exclude(id__in=Bet.objects.filter(player=player_id).values_list('game_id',flat=True))
                
        return queryset

class gameBetsView(LoginRequiredMixin,ListView):
    model = Game
    context_object_name = 'games'
    template_name = 'betting_app/games-bets.html'
    games = Game.objects.all().order_by("-date")

    queryset = games
    paginate_by = 6

class games(ListView):
    model = Game
    context_object_name = 'games'
    template_name = 'betting_app/games.html'
    games = Game.objects.all().order_by('-date')

    queryset = games
    paginate_by = 10

@login_required
def game(request, slug=None):
    game = get_object_or_404(Game, slug=slug)
  
    return render(request, 'betting_app/game.html', {'game': game})

class bets(LoginRequiredMixin,ListView):
    model = Bet
    context_object_name = 'bets'
    template_name = 'betting_app/bets.html'
    bets = Bet.objects.all().order_by('-created_date')

    queryset = bets
    paginate_by = 10

class my_bets(LoginRequiredMixin,ListView):
    model = Bet
    template_name = 'betting_app/my-bets.html'  
    paginate_by = 10

    def get_queryset(self):

        player_id = None
        user_id = self.request.user.id #logged user id
        if user_id:
            player = Player.objects.select_related("user").values("id").filter(user_id=user_id).get() #get player based on logged user id
            player_id = int(player['id'])
            if player_id is not None:
                queryset = Bet.objects.all().order_by('-created_date').filter(player=player_id)
                         
        return queryset

@login_required
def bet(request, pk):
    bet = get_object_or_404(Bet, pk=pk)
    return render(request, 'betting_app/bet.html', {'bet': bet})

@login_required
def new_game(request):

    form = GameForm()
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games-list')
        
    context = {'form':form}
    return render(request, 'betting_app/new-game.html', context)

@login_required
def update_game(request,pk):
    game = Game.objects.get(id=pk)
    form = UpdateGameForm(instance=game)

    if request.method == "POST":
        form = UpdateGameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Game has been updated')
            return redirect('games')
        
    context = {'form':form}
    return render(request, 'betting_app/new-game.html', context)

@login_required
def delete_game(request,pk):
    game = Game.objects.get(id=pk)

    if request.method == "POST":
        game.delete()
        return redirect('games')
        
    context = {'game':game}
    return render(request, 'betting_app/delete-game.html', context)

@login_required
def new_bet(request):

    context = {}
    pcount = Player.objects.count()
    if pcount > 0:
        player_id = ""
        user_id = request.user.id #logged user id
        if user_id:
            player = Player.objects.select_related("user").values("id").filter(user_id=user_id).get() #get player based on logged user id
            player_id = int(player['id'])

        obj = Player.objects.get(id=player_id)

        initial = {}
        if request.GET:
            initial = request.GET.copy()

        form = BetForm(initial=initial)
        if request.method == "POST":
            form = BetForm(request.POST)
            if form.is_valid():
                bet = form.save(commit=False)
                bet.player = obj
                bet.save()
                messages.add_message(request, messages.WARNING, 'Bet has been created!')
                return redirect('games')
        
        context = {'form':form}
    return render(request, 'betting_app/new-bet.html', context)

def login_user(request):
    return render(request, "registration/login.html")

@login_required
def logout_user(request):
    logout(request)
    return render(request, "registration/logout.html")

@login_required
def user_profile(request):
    
    context = {}
    pcount = Player.objects.count()
    if pcount > 0:   
        player_id = ""
        user_id = request.user.id #logged user id
        if user_id:
            player = Player.objects.select_related("user").values("id").filter(user_id=user_id).get() #get player based on logged user id
            player_id = int(player['id'])

        obj = Player.objects.get(id=player_id)

        #user points
        points = Bet.objects.filter(player=player_id).aggregate(Sum('score'))['score__sum']
   
    context['player'] = obj
    context['points'] = points
    
    pl = Player.objects.get(id=obj.id)
    form = ProfileUpdateForm(instance=pl)
    context['form'] = form
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=pl)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Your profile has been updated')
            return redirect('profile')

        context['form'] = form
        print(context)
    return render(request, "betting_app/profile.html", context)


class scores(LoginRequiredMixin,ListView):
    model = Bet
    context_object_name = 'data'
    template_name = 'betting_app/scores.html' 
    paginate_by = 10

    def get_queryset(self):
        queryset = Bet.objects.select_related("game").values("game__id", "game__slug","id", "player__nickname", "game", "game__home_team__name", "game__away_team__name", "game__league__name", "game__date", "game__home_goals", "game__away_goals", 
                                                     "home_goals", "away_goals", "game__result", "result", "created_date", "score", "game__round__name").order_by('game__round__name')

        if 'round' in self.request.GET:
            round = self.request.GET['round']
            if round:
                queryset = queryset.filter(game__round__name__icontains=round)

        return queryset
    

class my_bets(LoginRequiredMixin,ListView):
    model = Bet
    context_object_name = 'bets'
    template_name = 'betting_app/my-bets.html'

    paginate_by = 10
    
    def get_queryset(self):
        queryset = {}
        pcount = Player.objects.count()
        if pcount > 0:
            player_id = None
            user_id = self.request.user.id #logged user id
            if user_id:
                player = Player.objects.select_related("user").values("id").filter(user_id=user_id).get() #get player based on logged user id
                player_id = int(player['id'])
                if player_id is not None:
                    queryset = Bet.objects.all().order_by('-created_date').filter(player=player_id)
                         
        return queryset
    
@login_required
def ranking(request):
    
    players = Player.objects.all()

    rank = []
    for p in players:
        sum = Bet.objects.filter(player__nickname=p.nickname).values('score').aggregate(score_sum=Coalesce(Sum('score'),0))
        obj = {}
        obj['image'] = p.image
        obj['nickname'] = p.nickname
        obj['score'] = sum['score_sum']
        rank.append(obj)
   
    ranking = sorted(rank, key=itemgetter('score'), reverse=True)

    return render(request, "betting_app/ranking.html", {'ranking': ranking})

class newRound(CreateView, LoginRequiredMixin):
  
    model = Round
    fields = ['name']
    success_url = reverse_lazy('games-list')
    template_name = "betting_app/new-round.html"

def csv_export(request):

    data = Bet.objects.select_related("game").values("game__id", "game__slug","id", "player__nickname", "game", "game__home_team__name", "game__away_team__name", "game__league__name", "game__date", "game__home_goals", "game__away_goals", 
                                                     "home_goals", "away_goals", "game__result", "result", "created_date", "score", "game__round__name").order_by('game__round__name')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Player', 'Home team', 'Away team', 'League', 'Date', 'Game goals (home)', 'Game goals (away)', 'Bet goals (home)', 'Bet goals (away)', 'Game result' ,'Bet result' ,'Bet date', 'Points', 'Round'])
    for i in data:
        writer.writerow([i['player__nickname'], i['game__home_team__name'], i['game__away_team__name'], i['game__league__name'], i['game__date'],i['game__home_goals'],i['game__away_goals'],i['home_goals'],i['away_goals'],i['game__result'],i['result'], i['created_date'],i['score'],i['game__round__name']])
    return response
