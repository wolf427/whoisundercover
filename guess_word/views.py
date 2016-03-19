from django.shortcuts import render
from guess_word.service import get_word
from guess_word import wechat

# Create your views here.
def get_rondom_word():
    return wechat.formate_guess_reply(get_word().word_content)
