
from .models import Player

def user_processor(request):
    
    context = {}
    pcount = Player.objects.count()
    if pcount > 0:
        obj = None
        if request.user.id: 
            player_id = ""
            user_id = request.user.id #logged user id
            player = Player.objects.select_related("user").values("id").filter(user_id=user_id).get() #get player based on logged user id
            player_id = int(player['id'])
            obj = Player.objects.get(id=player_id)
            
            context = {'player': obj}

    return context
