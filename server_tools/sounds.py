import os
import modules.pytools as pytools
import time
from threading import Timer

def getSoundCopyCounts(host, printf=False):
    lsf = {}
    total = 0
    for sound in os.listdir("\\\\" + host + "\\ambience\\vars\\pluginSounds"):
        try:
            data = pytools.IO.getFile("\\\\" + host + "\\ambience\\vars\\pluginSounds\\" + sound).split(";")
            total = total + 1
            if data[0] not in lsf:
                lsf[data[0]] = 1
            else:
                lsf[data[0]] = lsf[data[0]] + 1
        except:
            print("Sound deleted. " + sound)
    
    unsortedList = lsf.keys()
    
    def _iter(x):
        return lsf[x]
    
    sortedList = sorted(unsortedList, key=_iter, reverse=True)
    
    print("Total Sounds: " + str(total))
    
    if printf:
        for sound in sortedList:
            print(sound + "; " + str(lsf[sound]))
    else:
        return lsf
    
def dummy():
    pass
        
loopRange = [0] * 1000000

def intenseWait(i):
    x = time.time() + i
    while time.time() < x:
        pass

def intenseFor(i):
    x = time.time() + i
    for f in loopRange:
        if time.time() >= x:
            break

def timeingTest(g, ctf=1000):
    
    arTime = []
    arThread = []
    arIntense = []
    
    i = 0
    while i < ctf:
        ticf = time.time()
        time.sleep(g)
        arTime.append(time.time() - ticf)
        ticf = time.time()
        intenseWait(g)
        arIntense.append(time.time() - ticf)
        ticf = time.time()
        intenseFor(g)
        arThread.append(time.time() - ticf)
        i = i + 1
    
    print("timer: " + str(sum(arTime) / len(arTime)) + "/" + str(max(arTime) - min(arTime)) + ", intenseSleep: " + str(sum(arIntense) / len(arIntense)) + "/" + str(max(arIntense) - min(arIntense)) + ", intenseFor: " + str(sum(arThread) / len(arThread)) + "/" + str(max(arThread) - min(arThread)))