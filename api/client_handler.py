import modules.pytools as pytools
import time
import subprocess
import json
import urllib.parse
import traceback
import modules.audio as audio
import os
import modules.logManager as log

import threading

log.settings.debug = True

def doPrint(stuff):
    log.printLog(stuff)

print = doPrint

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }
    
class hosts:
    listf = pytools.IO.getJson("hosts.json")["hosts"]
    soundsf = {}
    soundsfOld = {}
    soundsfCache = {}
    benchCache = {}
    
    updateMaxCount = pytools.clock.getDateTime()[2]
    
    hasUpdated = False
    
    listOfHosts = {}
    
class hostObject:
    def __init__(self, hostName):
        self.host = hostName
        
        self.isRunning = True
        
        self.declareTime = time.time()
    
    updateMaxCount = -1
    
    def run(self):
        try:
            print("Checking if host " + self.host + "exists...")
            try:
                hosts.soundsf[self.host]
                print("Host exists.")
            except:
                if self.host not in hosts.soundsfCache:
                    print("Host does not exist. Generating data...")
                    hosts.soundsf[self.host] = {
                        "max": 0,
                        "current": 0,
                        "play": False
                    }
                    hasUpdated = True
                else:
                    print("Host does not exist. Grabbing data from cache...")
                    hosts.soundsf[self.host] = hosts.soundsfCache[self.host]
                    hasUpdated = True
            
            if (hosts.soundsf[self.host]["max"] == 0):
                print("Host has not maximum. Testing benchmark...")
                try:
                    print("    > Saving bm file...")
                    pytools.IO.saveFile(".\\host-" + self.host + ".bm", "")
                    print("    > Sending stop command to host...")
                    audio.command.sendStop(target=self.host)
                    print("    > Waiting...")
                    time.sleep(5)
                    print("    > Testing benchmark...")
                    # if host not in hosts.benchCache:
                    maxf = pytools.net.getJsonAPI("http://" + self.host + ":4507?json=" + urllib.parse.quote(json.dumps({
                        "command": "getMaxSoundCount"
                    })), timeout=30)["maxSoundCount"] * 0.4
                    if maxf > 0:
                        maxf = maxf ** 0.9
                        # if maxf != 0:
                            # hosts.benchCache[host] = maxf
                    # else:
                        # maxf = hosts.benchCache[host]
                    print("Deleting bm file...")
                    os.system("del \".\\host-" + self.host + ".bm\" /f /q")
                    print("Benchmark tested.")
                except:
                    print(traceback.format_exc())
                    maxf = 0
                print("Current benchmark for host " + self.host + " is " + str(maxf) + ".")
                if hosts.soundsf[self.host]["max"] != maxf:
                    hosts.hasUpdated = True
                hosts.soundsf[self.host]["max"] = maxf
                
            if pytools.clock.getDateTime()[3] != self.updateMaxCount:
                try:
                    print("Host data is stale. Testing benchmark...")
                    print("    > Testing benchmark...")
                    maxf = pytools.net.getJsonAPI("http://" + self.host + ":4507?json=" + urllib.parse.quote(json.dumps({
                        "command": "getMaxSoundCount"
                    })), timeout=10)["maxSoundCount"] * 0.4
                    if maxf > 0:
                        maxf = maxf ** 0.9
                    print("Benchmark tested.")
                    if hosts.soundsf[self.host]["max"] != maxf:
                        hosts.hasUpdated = True
                    hosts.soundsf[self.host]["max"] = maxf
                except:
                    print(traceback.format_exc())
                self.updateMaxCount = pytools.clock.getDateTime()[3]
            
            try:
                print("Grabbing current sound count...")
                currentf = pytools.net.getJsonAPI("http://" + self.host + ":4507?json=" + urllib.parse.quote(json.dumps({
                    "command": "getSoundCount"
                })), timeout=5)["soundCount"] + pytools.net.getJsonAPI("http://" + self.host + ":4507?json=" + urllib.parse.quote(json.dumps({
                    "command": "getSoundQueSize"
                })), timeout=5)["SoundQueSize"]
                print("Current sound count for host " + self.host + " is " + str(currentf) + ".")
            except:
                print("Error grabbing sound count. Setting to maximum...")
                currentf = maxf
            if hosts.soundsf[self.host]["current"] != currentf:
                hasUpdated = True
            hosts.soundsf[self.host]["current"] = currentf
            print("Saved.")
            
            if hosts.soundsf[self.host]["current"] >= hosts.soundsf[self.host]["max"]:
                print("WARNING: Host Overload Detected! Preventing sound plays on host " + self.host + "...")
                if hosts.soundsf[self.host]["play"]:
                    hasUpdated = True
                hosts.soundsf[self.host]["play"] = False
            else:
                print("Host is not overloaded.")
                if not hosts.soundsf[self.host]["play"]:
                    hasUpdated = True
                hosts.soundsf[self.host]["play"] = True
        except:
            print(traceback.format_exc())
        self.isRunning = False

def main():
    loopCount = 0
    while not status.exit:
        print("Grabbing host list...")
        try:
            listf = pytools.IO.getJson("hosts.json")["hosts"]
            print("Grabbed.")
        except:
            listf = []
        
        if listf != 1:
            print("Is correct data. Saving...")
            hosts.listf = listf
        
        for host in hosts.listf:
            hostObjectInstance = hostObject(host)
            if host not in hosts.listOfHosts:
                hosts.listOfHosts[host] = [hostObjectInstance, False]
                hosts.listOfHosts[host][1] = threading.Thread(target=hosts.listOfHosts[host][0].run)
                hosts.listOfHosts[host][1].start()
            elif (hosts.listOfHosts[host][0].isRunning == False) or ((hosts.listOfHosts[host][0].declareTime + 20000) > (time.time())):
                hosts.listOfHosts[host] = [hostObjectInstance, False]
                hosts.listOfHosts[host][1] = threading.Thread(target=hosts.listOfHosts[host][0].run)
                hosts.listOfHosts[host][1].start()
        
        print("Testing hosts to remove...")
        hostsToRemove = []
        for host in hosts.soundsf:
            if host not in hosts.listf:
                print("Host " + host + " detected as offline. Removing...")
                hosts.soundsfCache[host] = hosts.soundsf[host]
                hostsToRemove.append(host)
                hosts.hasUpdated = True
                
        for host in hostsToRemove:
            print("Host " + host + " has been removed.")
            hosts.soundsf.pop(host)

        print("Testing hostData.json file...")
        if hosts.hasUpdated:
            print("Saving hostData.json file...")
            pytools.IO.saveJson(".\\hostData.json", hosts.soundsf)
            hosts.soundsfOld = hosts.soundsf
            
        time.sleep(1)
        status.finishedLoop = True
        status.vars["lastLoop"] = pytools.clock.getDateTime()
        
def run():
    status.hasExited = False
    main()
    status.hasExited = True