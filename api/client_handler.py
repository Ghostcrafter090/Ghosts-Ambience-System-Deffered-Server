import modules.pytools as pytools
import time
import subprocess
import json
import urllib.parse
import traceback
import modules.audio as audio
import os
import modules.logManager as log
import modules.audio as audio

def doPrint(stuff):
    if False:
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
            print("Checking if host " + host + "exists...")
            try:
                hosts.soundsf[host]
                print("Host exists.")
            except:
                if host not in hosts.soundsfCache:
                    print("Host does not exist. Generating data...")
                    hosts.soundsf[host] = {
                        "max": 0,
                        "current": 0,
                        "play": False
                    }
                    hasUpdated = True
                else:
                    print("Host does not exist. Grabbing data from cache...")
                    hosts.soundsf[host] = hosts.soundsfCache[host]
                    hasUpdated = True
            
            if hosts.soundsf[host]["max"] == 0:
                print("Host has not maximum. Testing benchmark...")
                try:
                    print("    > Saving bm file...")
                    pytools.IO.saveFile(".\\host-" + host + ".bm", "")
                    print("    > Sending stop command to host...")
                    audio.command.sendStop(target=host)
                    print("    > Waiting...")
                    time.sleep(5)
                    print("    > Testing benchmark...")
                    maxf = pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                        "command": "getMaxSoundCount"
                    })), timeout=30)["maxSoundCount"] * 0.6
                    print("Deleting bm file...")
                    os.system("del \".\\host-" + host + ".bm\" /f /q")
                    print("Benchmark tested.")
                except:
                    maxf = 0
                print("Current benchmark for host " + host + " is " + str(maxf) + ".")
                if hosts.soundsf[host]["max"] != maxf:
                    hasUpdated = True
                hosts.soundsf[host]["max"] = maxf
            
            try:
                print("Grabbing current sound count...")
                currentf = pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                    "command": "getSoundCount"
                })), timeout=30)["soundCount"]
                print("Current sound count for host " + host + " is " + str(currentf) + ".")
            except:
                print("Error grabbing sound count. Setting to maximum...")
                currentf = maxf
            if hosts.soundsf[host]["current"] != currentf:
                hasUpdated = True
            hosts.soundsf[host]["current"] = currentf
            print("Saved.")
            
            if hosts.soundsf[host]["current"] >= hosts.soundsf[host]["max"]:
                print("WARNING: Host Overload Detected! Preventing sound plays on host " + host + "...")
                if hosts.soundsf[host]["play"]:
                    hasUpdated = True
                hosts.soundsf[host]["play"] = False
            else:
                print("Host is not overloaded.")
                if not hosts.soundsf[host]["play"]:
                    hasUpdated = True
                hosts.soundsf[host]["play"] = True
        
        print("Testing hosts to remove...")
        hostsToRemove = []
        for host in hosts.soundsf:
            if host not in hosts.listf:
                print("Host " + host + " detected as offline. Removing...")
                hosts.soundsfCache[host] = hosts.soundsf[host]
                hostsToRemove.append(host)
                hasUpdated = True
                
        for host in hostsToRemove:
            print("Host " + host + " has been removed.")
            hosts.soundsf.pop(host)

        print("Testing hostData.json file...")
        if hasUpdated:
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