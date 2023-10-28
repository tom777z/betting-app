from django.urls import path
from . import views
from betting_app.views import indexView
from django.views.decorators.cache import never_cache

urlpatterns = [ 
    
    path('', never_cache(views.indexView.as_view()), name="games"),
    path('games/', views.games.as_view(), name="games-list"),
    path('bets', views.bets.as_view(), name="bets"),
    path('my-bets', views.my_bets.as_view(), name="my-bets"),
    path('game-bets', views.gameBetsView.as_view(), name="game-bets"),
    path('new-game/', views.new_game, name="new-game"),
    path('update-game/<str:pk>/', views.update_game, name="update-game"),
    path('delete-game/<str:pk>/', views.delete_game, name="delete-game"),
    path('new-bet/', views.new_bet, name="new-bet"),
    path('game/<slug:slug>/', views.game, name='game'),
    path('bet/<int:pk>/', views.bet, name='bet'),
    path('scores/', views.scores.as_view(), name="scores"),
    path('ranking/', views.ranking, name="ranking"),
    path('new-round', views.newRound.as_view(), name="new-round"),
    path('login/', views.login_user, name="login"),
    path('accounts/logout/', views.logout_user, name="logout"),
    path('profile/', views.user_profile, name="profile"),
]