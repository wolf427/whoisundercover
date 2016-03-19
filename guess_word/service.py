# -*- coding: utf-8 -*-
'''
Created on 2016年3月19日

@author: wolf
'''
from guess_word.models import Word
import random
def get_word():
    randomIndex = random.randint(0, Word.objects.all().count() - 1)
    return Word.objects.all()[randomIndex:randomIndex + 1][0]