import modules.pytools as pytools
import time
import subprocess
import json
import urllib.parse
import traceback
import modules.audio as audio
import os
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
    
class hosts:
    listf = pytools.IO.getJson("hosts.json")["hosts"]
    soundsf = {}

def main():
    loopCount = 0
    while not status.exit:
        
        try:
            if pytools.IO.getFile("..\\hosts.json") != pytools.IO.getFile(".\\hosts.json"):
                pytools.IO.saveFile(".\\hosts.json", pytools.IO.getFile("..\\hosts.json"))
        except:
            pass
        
        hosts.listf = pytools.IO.getJson("hosts.json")["hosts"]
        count = str(len(subprocess.getoutput("tasklist /fi \"IMAGENAME eq ambience.exe\" /fo:csv").split("\n")))
        pytools.IO.saveFile("soundCount.cx", count)
        print("Total Sounds: " + count)
        if (hosts.soundsf == {}) or (str(hosts.soundsf)[0] != "{"):
            soundsf = pytools.IO.getJson(".\\hostData.json")
            if str(soundsf)[0] != "{":
                if str(hosts.soundsf)[0] != "{":
                    hosts.soundsf = {}
            else:
                hosts.soundsf = soundsf
        for puppet in hosts.listf:
            try:
                puppetMax = hosts.soundsf[puppet]["max"]
                if puppetMax == 0:
                    try:
                        pytools.IO.saveFile(".\\host-" + puppet + ".bm", "")
                        audio.command.sendStop(target=puppet)
                        time.sleep(3)
                        puppetMax = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                            "command": "getMaxSoundCount"
                        })), timeout=30)["maxSoundCount"] * 0.6,
                        os.system("del \".\\host-" + puppet + ".bm\" /f /q")
                    except:
                        os.system("del \".\\host-" + puppet + ".bm\" /f /q")
                        puppetMax = 0
                        print(traceback.format_exc())
            except:
                print(traceback.format_exc())
                print(hosts.soundsf)
                try:
                    pytools.IO.saveFile(".\\host-" + puppet + ".bm", "")
                    audio.command.sendStop(target=puppet)
                    time.sleep(3)
                    puppetMax = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                        "command": "getMaxSoundCount"
                    })), timeout=30)["maxSoundCount"] * 0.6,
                    os.system("del \".\\host-" + puppet + ".bm\" /f /q")
                except:
                    os.system("del \".\\host-" + puppet + ".bm\" /f /q")
                    puppetMax = 0
                    print(traceback.format_exc())
            print(puppetMax)
            try:
                hosts.soundsf[puppet]["max"] = puppetMax
                hosts.soundsf[puppet]["current"] = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                    "command": "getSoundCount"
                })), timeout=30)["soundCount"]
                hosts.soundsf[puppet]["play"] =  False
            except:
                print(traceback.format_exc())
            try:
                if str(hosts.soundsf[puppet]["max"])[0] == "(":
                    hosts.soundsf[puppet]["max"] = hosts.soundsf[puppet]["max"][0]
                if hosts.soundsf[puppet]["max"] >= hosts.soundsf[puppet]["current"]:
                    hosts.soundsf[puppet]["play"] = True
            except:
                print(traceback.format_exc())
            try:
                pytools.IO.saveJson(".\\hostData.json", hosts.soundsf)
            except:
                print(traceback.format_exc())
        try:
            pass
            # oldHostData = pytools.IO.getJson(".\\hostData.json")
            # removeHosts = []
            # for host in hosts.soundsf:
            #     if host not in oldHostData:
            #         removeHosts.append(host)
            # for host in removeHosts:
            #     hosts.soundsf.pop(host)
            # pytools.IO.saveJson(".\\hostData.json", hosts.soundsf)
        except:
            print(traceback.format_exc())
        if loopCount > 15:
            for host in hosts.listf:
                errorCount = 0
                try:
                    connect = pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                            "command": "ping"
                        })), timeout=1)["status"] == "success"
                except:
                    connect = False
                while not connect:
                    try:
                        connect = pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                            "command": "ping"
                        })), timeout=1)["status"] == "success"
                    except:
                        connect = False
                    errorCount = errorCount + 1
                if errorCount > 100:    
                    hosts.listf.remove(host)
                    os.system("del \".\\host-" + host + ".bm\" /f /q")
                pytools.IO.saveJson("hosts.json", {
                    "hosts": hosts.listf
                })
                pytools.IO.saveJson("..\hosts.json", {
                    "hosts": hosts.listf
                })
            loopCount = 0
        loopCount = loopCount + 1
        time.sleep(1)
        status.finishedLoop = True
        status.vars["lastLoop"] = pytools.clock.getDateTime()
        
def run():
    status.hasExited = False
    main()
    status.hasExited = True