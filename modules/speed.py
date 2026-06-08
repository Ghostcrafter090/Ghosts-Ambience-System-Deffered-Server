import sys
import math
import random
import time
import threading
import modules.flame as flame
import traceback
import os

class vars:
    prevTic = False
    thread = False
    counterThread = False
    waitTic = 0.001
    intf = 0.005
    threadCount = 0
    
def threadCounter():
    time.sleep(10)
    while True:
        try:
            vars.threadCount = flame.getNumberOfThreads(flame.getSnapshot())
            time.sleep(10)
        except:
            print(traceback.format_exc())
    
def sysHandler():
    
    prevDo = False
    
    while True:
        beforeTic = time.time()
        time.sleep(vars.waitTic)
        math.fabs((random.random() - 0.5) * 10)
        afterTic = time.time()
        if not vars.prevTic:
            vars.prevTic = afterTic - beforeTic
        else:
            
            if vars.prevTic > (afterTic - beforeTic):
                if prevDo:
                    if (vars.intf - 0.000001) > 0.000002:
                        vars.intf = vars.intf - 0.000001
                else:
                    if (vars.intf + 0.000001) < 0.5:
                        vars.intf = vars.intf + 0.000001
            
            if random.random() < 0.5:
                prevDo = True
                if (vars.intf + 0.000001) < 0.5:
                    vars.intf = vars.intf + 0.000001
            else:
                prevDo = False
                if (vars.intf - 0.000001) > 0.000002:
                    vars.intf = vars.intf - 0.000001
            vars.prevTic = (afterTic - beforeTic)
            
        if vars.intf < 0.001:
            vars.intf = 0.001
            
        sys.setswitchinterval(vars.intf)
        
def run(doThreadCounter=True):
    vars.thread = threading.Thread(target=sysHandler)
    vars.thread.start()
    if doThreadCounter:
        vars.counterThread = threading.Thread(target=threadCounter)
        vars.counterThread.start()