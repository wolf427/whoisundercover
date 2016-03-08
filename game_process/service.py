'''
@author: wolf
'''
from game_process.models import User,Room,PhraseEntry,RoomPhraseRelation,RoomPhraseRelation
import random
def initRoom(userName,userCount):
    User.objects.get_or_create(userName)
    while :
        random.randint(1000,9999)
    
    