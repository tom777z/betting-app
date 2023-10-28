from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Bet
from .views import calculate_score

@receiver(post_save, sender=Game)
def action_when_goals_updated(sender, instance, created, **kwargs):
    if created:
        if instance.home_goals is not None and instance.away_goals is not None:
            Game.objects.filter(id=instance.pk).update(active=False)    #deactivate game record if results are provided on creation
                                                          
    if not created:
        if instance.home_goals is not None and instance.away_goals is not None:
            Game.objects.filter(id=instance.pk).update(active=False)    #deactivate game record if results are provided on update
            
            ''' calculate bets scores each time game record is updated'''
            bets = Bet.objects.select_related("game").values("game__id", "id", "home_goals", "away_goals", "result").filter(game=instance.pk)
            score = 0
            for i, bet in enumerate(bets):
                
                b_id = bet['id']
                g_id = bet['game__id']
                b_hg = bet['home_goals']
                b_ag = bet['away_goals']
                b_r = bet['result']

                game = Game.objects.filter(id=g_id).values()
                g_hg = game[0]['home_goals']
                g_ag = game[0]['away_goals']
                g_r = game[0]['result']
                
                score = calculate_score(b_hg, b_ag, b_r, g_hg, g_ag, g_r)
                Bet.objects.filter(id=b_id).update(score=score)  
            ''' end '''

        elif instance.home_goals is None and instance.away_goals is None:
            Game.objects.filter(id=instance.pk).update(active=True)  #activate game record if results are empty  

            ''' reset existing bets scores if game results are empty'''
            bets = Bet.objects.select_related("game").values("id", "game").filter(game=instance.pk)
            score = None
            for i, bet in enumerate(bets):
                
                b_id = bet['id']                
                Bet.objects.filter(id=b_id).update(score=score) 
            ''' end'''