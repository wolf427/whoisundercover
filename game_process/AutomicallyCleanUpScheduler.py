'''
Created on Mar 10, 2016

@author: yufeitan
'''
import sched, time
from game_process.service import automicallyCleanUp
from django.shortcuts import render
s = sched.scheduler(time.time, time.sleep)

def autoCleanUp(inc): 
    s.enter(inc, 1, autoCleanUp, (inc,))
    automicallyCleanUp()
    

def startAutoSche(req):
    print "init_clean"
    inc = 1800
    s.enter(0, 1, autoCleanUp, (inc,))
    s.run()
    return render("success")
    
    
