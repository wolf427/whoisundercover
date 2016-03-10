'''
Created on Mar 10, 2016

@author: yufeitan
'''
import sched, time
from game_process.service import automicallyCleanUp

s = sched.scheduler(time.time, time.sleep)

def autoCleanUp(inc): 
    s.enter(inc, 1, autoCleanUp, (inc,))
    automicallyCleanUp()
    

def startAutoSche():
    inc = 1800
    s.enter(0, 1, autoCleanUp, (inc,))
    s.run()
    
