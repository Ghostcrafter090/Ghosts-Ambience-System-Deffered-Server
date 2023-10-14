import modules.audio as audio
import modules.pytools as pytools
import os
import time
import math
import modules.logManager as log

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }
    
class globals:
    frozenPercentage = 0
    frozenDepth = 0

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, "", 0, 0, 15, 0], [0, 0, 0, 0, 0, 0]]
        return out
    
    def testWindow():
        out = 0
        if os.path.exists(".\\nomufflewn.derp") == True:
            out = 1
        return out

def main():
    
    if os.path.exists("lake_ice.json"):
        try:
            jsonData = pytools.IO.getJson("lake_ice.json")
            globals.frozenPercentage = jsonData["frozenPercentage"]
            globals.frozenDepth = jsonData["frozenDepth"]
        except:
            print("Could not grab frozen data.")
    
    while not status.exit:
        error = 1
        while error == 1:
            try:
                data = utils.dataGrabber()
                pytools.dummy(str(data[0][1]))
                error = 0
            except:
                error = 1
                no = 1
        t = data[0][7]
        h = data[0][8]
        w = t * math.atan(0.151977 * (h + 8.313659) ** (((1) / (2)))) + math.atan(t + h) - math.atan(h * 1.676331) + 0.00391838 * (h) ** (((3) / (2))) * math.atan(0.023101 * h) - 4.686035
        
        status.vars["wetBulbTemp"] = w
        
        if w < 0:
            if globals.frozenPercentage < 100:
                globals.frozenPercentage = globals.frozenPercentage + (0.08333333333333333 * (-w))
            else:
                globals.frozenDepth = globals.frozenDepth + (0.00125 * (-w))
                
        if w > 0:
            if globals.frozenDepth >= 0:
                globals.frozenDepth = globals.frozenDepth - (0.00125 * (w))
            else:
                globals.frozenPercentage = globals.frozenPercentage - (0.08333333333333333 * (w))
        
        if globals.frozenDepth > 45:
            globals.frozenDepth = 45
        
        if globals.frozenPercentage < 0:
            globals.frozenPercentage = 0
        
        if globals.frozenDepth < 0:
            globals.frozenDepth = 0
            
        pytools.IO.saveJson("lake_ice.json", {
            "frozenPercentage": globals.frozenPercentage,
            "frozenDepth": globals.frozenDepth
        })
        
        status.vars["frozenPercentage"] = globals.frozenPercentage
        status.vars["frozenDepth"] = globals.frozenDepth
        
        print(status.vars)
        
        volume = 0.837021 ** ( - 0.350364 * (globals.frozenDepth + 29.8758)) - 6.39628
        volume = volume / 2
        
        volume = (volume ** 0.6) * 4.781762498950186
        
        speed = 0.966807 ** ( - 0.00043857 * (globals.frozenDepth + 93484.5)) - 1.92647 * globals.frozenDepth ** (0.179284)
        
        if globals.frozenPercentage >= 100:
            if globals.frozenDepth > 0:
                print("Playing winter ice sound...")
                audioEvent = audio.event()
                audioEvent.register('ice_wall.mp3', 0, volume / 4, speed, 0, 0)
                audioEvent.register('ice_wall.mp3', 1, volume / 4, speed, 0, 0)
                audioEvent.registerWindow('ice_wn.mp3;ice_nm.mp3', [volume / 2, volume, volume], speed, 0, 0)
                audioEvent.run()
            
        time.sleep(300 / speed)
        
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
