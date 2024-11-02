import voicemeeter
import sounddevice as sd
import time
import os
import psutil
import modules.pytools as pytools
import subprocess
import urllib.parse
import json
import traceback
import modules.audio as audio
import random
import copy
import sys

import modules.logManager as log
import modules.vban as vban

print = log.printLog

log.settings.debug = True

class globals:
    instance = False
    mme = 2048
    wdm = 1024
    noChange = True
    started = False

class server:
    
    hostname = "0.0.0.0"
    interface = "0.0.0.0"
    
    class con:
        def arp():
            ipsDirty = subprocess.getoutput("arp -a -v").split("\n")
            try:
                interfaceBlacklist = pytools.IO.getJson("excludeInterfaces.json")["list"]
            except:
                interfaceBlacklist = []
            ips = {}
            for entry in ipsDirty:
                if entry.find("Interface:") != -1:
                    interface = entry.split("Interface: ")[1].split(" ")[0]
                    if not interface in interfaceBlacklist:
                        ips[interface] = []
                elif entry.find("Internet Address") != -1:
                    pass
                else:
                    try:
                        entryf = entry.split(" ")
                        while '' in entryf:
                            entryf.remove('')
                        if not interface in interfaceBlacklist:
                            ips[interface].append(entryf[0])
                    except:
                        pass
            return ips
        
        def connect():
            oldSettings = pytools.IO.getJson("serverSettings.json")
            try:
                print("Attempting to connect to last known ip address " + oldSettings["ip"] + "...")
                pytools.net.getJsonAPI("http://" + oldSettings["interface"] + ":4507?json=" + urllib.parse.quote(json.dumps({
                    "command": "ping"
                })), timeout=1)
                pytools.net.getJsonAPI("http://" + oldSettings["ip"] + ":5597?json=" + urllib.parse.quote(json.dumps({
                    "command": "ping",
                    "data": {
                        "ipAddress": oldSettings["interface"]
                    }
                })), timeout=1)
                outIp = [oldSettings["ip"], oldSettings["interface"]]
            except:
                finished = False
                while not finished:
                    arp = server.con.arp()
                    for interface in server.con.arp():
                        try:
                            print("Attempting to connect to ip address " + ip + "...")
                            pytools.net.getJsonAPI("http://" + interface + ":5597?json=" + urllib.parse.quote(json.dumps({
                                "command": "ping",
                                "data": {
                                    "ipAddress": interface
                                }
                            })), timeout=1)
                            outIp = [interface, interface]
                            finished = True
                            break
                        except:
                            print("Failed to connect.")
                        for ip in arp[interface]:
                            try:
                                print("Attempting to connect to ip address " + ip + "...")
                                pytools.net.getJsonAPI("http://" + ip + ":5597?json=" + urllib.parse.quote(json.dumps({
                                    "command": "ping",
                                    "data": {
                                        "ipAddress": interface
                                    }
                                })), timeout=1)
                                outIp = [ip, interface]
                                finished = True
                                break
                            except:
                                print("Failed to connect.")
                pytools.IO.saveJson("serverSettings.json", {
                    "ip": outIp[0],
                    "interface": outIp[1]
                })
            return outIp
    
    def startConnection():
        con = server.con.connect()
        server.hostname = con[0]
        server.interface = con[1]
    
    def grabOtherComputers():
        try:
            return pytools.net.getJsonAPI("http://localhost:5597?json=" + urllib.parse.quote(json.dumps({
                "command": "getOtherComputers"
            })), timeout=1)
        except:
            print("Connection Failed.")
            while True:
                # server.startConnection()
                try:
                    return pytools.net.getJsonAPI("http://localhost:5597?json=" + urllib.parse.quote(json.dumps({
                        "command": "getOtherComputers"
                    })), timeout=1)
                except:
                    print("Connection Failed.")

class vm:
    changed = False
    
    def checkStatus():
        try:
            globals.instance.get("option.buffer.mme")
        except:
            print("regrabbing...")
            vm.launch()
            globals.instance = voicemeeter.remote("potato")
            globals.instance.login()
            vm.changed = True
        
    def launch():
        if os.path.exists("C:\Program Files (x86)\VB\Voicemeeter\\voicemeeter8.exe"):
            if os.path.exists("..\Voicemeeter.lnk"):
                if ("voicemeeter8.exe" in (p.name() for p in psutil.process_iter())) == False:
                    os.system("taskkill /f /im voicemeeter8.exe")
                    os.system('start /b "" ..\Voicemeeter.lnk')
            else:
                if ("voicemeeter8.exe" in (p.name() for p in psutil.process_iter())) == False:
                    installDate = pytools.clock.getDateArrayFromUST(os.path.getctime("C:\Program Files (x86)\VB\Voicemeeter\\voicemeeter8.exe"))
                    os.system("start /d \"C:\Program Files (x86)\VB\Voicemeeter\" \"\" RunAsDate.exe /immediate /movetime " + str(installDate[2]) + "\\" + str(installDate[1]) + "\\" + str(installDate[0]) + " " + str(installDate[3]) + ":" + str(installDate[4]) + ":" + str(installDate[5]) + " \"C:\\Program Files (x86)\\VB\\Voicemeeter\\voicemeeter8.exe\"")
        time.sleep(5)
        
    def handler():
        while True:
            try:
                configure.fixAudioDg()
            except:
                pass
            try:
                vm.checkStatus()
            except:
                pass
            time.sleep(1)    

class configure:
    def fixAudioDg():
        audioDgSize = float(subprocess.getoutput('tasklist /fi "IMAGENAME eq audiodg.exe" /fo csv').split("\n")[1].split("\",\"")[-1].replace(",", "").replace(" K\"", ""))
        if audioDgSize > 1000000.0:
            print("Oversized audiodg.exe detected. Resetting...")
            os.system("taskkill /f /im audiodg.exe")
            os.system("%windir%\\system32\\rundll32.exe advapi32.dll,ProcessIdleTasks")
            os.system('"C:\Program Files (x86)\VB\Voicemeeter\voicemeeter8.exe" -r')
    
    class local:
        def getOutputs():
            devices = sd.query_devices()
            out = {}
            outFinal = []
            sortedKey = []
            for device in devices:
                if device["name"].find("VB-Audio Virt") != -1:
                    if device["hostapi"] == 0:
                        if device["max_output_channels"] > 0:
                            out[device["name"]] = device
                            sortedKey.append([device["name"], device["name"].split("(")[1]])
            sortedKey = sorted(sortedKey, key = lambda s: sum(map(ord, s[1])), reverse=False)
            i = 0
            while i < len(sortedKey):
                outFinal.append(out[sortedKey[i][0]])
                i = i + 1
            clock = False
            fireplace = False
            window = False
            for device in devices:
                if device["name"] == "VoiceMeeter Input (VB-Audio Voi":
                    clock = True
                if device["name"] == "VoiceMeeter Aux Input (VB-Audio":
                    fireplace = True
                if device["name"] == "VoiceMeeter VAIO3 Input (VB-Aud":
                    window = True
            
            soundOutputs = False
            if clock:
                if fireplace:
                    if window:
                        soundOutputs = {
                            "clock": ["VoiceMeeter Input (VB-Audio Voi", "MME"],
                            "fireplace": ["VoiceMeeter Aux Input (VB-Audio", "MME"],
                            "window": ["VoiceMeeter VAIO3 Input (VB-Aud", "MME"],
                            "outside": [outFinal[0]["name"], "MME"],
                            "porch": [outFinal[1]["name"], "MME"],
                            "generic": [outFinal[2]["name"], "MME"],
                            "light": [outFinal[3]["name"], "MME"]
                        }
            
            return soundOutputs
        
        def getInputs():
            devices = sd.query_devices()
            out = {}
            outFinal = []
            sortedKey = []
            for device in devices:
                if device["name"].find("VB-Audio Virt") != -1:
                    if device["hostapi"] == 0:
                        if device["max_input_channels"] > 0:
                            out[device["name"]] = device
                            sortedKey.append([device["name"], device["name"].split("(")[1]])
            sortedKey = sorted(sortedKey, key = lambda s: sum(map(ord, s[1])), reverse=False)
            i = 0
            while i < len(sortedKey):
                outFinal.append(out[sortedKey[i][0]])
                i = i + 1
            clock = False
            fireplace = False
            window = False
            for device in devices:
                if device["name"] == "VoiceMeeter Input (VB-Audio Voi":
                    clock = True
                if device["name"] == "VoiceMeeter Aux Input (VB-Audio":
                    fireplace = True
                if device["name"] == "VoiceMeeter VAIO3 Input (VB-Aud":
                    window = True
            
            soundInputs = False
            if clock:
                if fireplace:
                    if window:
                        soundInputs = {
                            "clock": ["VoiceMeeter Input (VB-Audio Voi", "MME"],
                            "fireplace": ["VoiceMeeter Aux Input (VB-Audio", "MME"],
                            "window": ["VoiceMeeter VAIO3 Input (VB-Aud", "MME"],
                            "outside": [outFinal[0]["name"], "MME"],
                            "porch": [outFinal[1]["name"], "MME"],
                            "generic": [outFinal[2]["name"], "MME"],
                            "light": [outFinal[3]["name"], "MME"]
                        }
            
            return soundInputs
        
        def setOutputs(fix=False):
            outputs = configure.local.getOutputs()
            pytools.IO.saveJson(".\\soundOutputs.json", outputs)
            if outputs:
                if globals.instance.inputs[0].device != configure.local.getInputs()["outside"][0]:
                    globals.instance.set("Strip[0].device.mme", configure.local.getInputs()["outside"][0])
                if globals.instance.inputs[1].device != configure.local.getInputs()["porch"][0]:
                    globals.instance.set("Strip[1].device.mme", configure.local.getInputs()["porch"][0])
                if globals.instance.inputs[2].device != configure.local.getInputs()["generic"][0]:
                    globals.instance.set("Strip[2].device.mme", configure.local.getInputs()["generic"][0])
                if globals.instance.inputs[3].device != configure.local.getInputs()["light"][0]:
                    globals.instance.set("Strip[3].device.mme", configure.local.getInputs()["light"][0])
                if globals.instance.get("Bus[0].device.name", string=True) != sd.query_devices()[sd.default.device[1]]["name"]:
                    if sd.query_devices()[sd.default.device[1]]["hostapi"] == 0:
                        globals.instance.set("Bus[0].device.mme", sd.query_devices()[sd.default.device[1]]["name"])
                    else:
                        globals.instance.set("Bus[0].device.wdm", sd.query_devices()[sd.default.device[1]]["name"])
                if globals.instance.inputs[5].A2 != True:
                    if globals.instance.inputs[6].A3 != True:
                        if globals.instance.inputs[7].A4 != True:
                            if globals.instance.inputs[0].A5 != True:
                                if globals.instance.inputs[1].B1 != True:
                                    if globals.instance.inputs[2].B2 != True:
                                        if globals.instance.inputs[3].B3 != True:
                                            for input in globals.instance.inputs:
                                                input.A1 = False
                                                input.A2 = False
                                                input.A3 = False
                                                input.A4 = False
                                                input.A5 = False
                                                input.B1 = False
                                                input.B2 = False
                                                input.B3 = False
                                                input.mute = False
                                            globals.instance.inputs[5].A2 = True
                                            globals.instance.inputs[6].A3 = True
                                            globals.instance.inputs[7].A4 = True
                                            globals.instance.inputs[0].A5 = True
                                            globals.instance.inputs[1].B1 = True
                                            globals.instance.inputs[2].B2 = True
                                            globals.instance.inputs[3].B3 = True
            vm.changed = False
    
    class vban:
        clientsOld = []
        
        def getDaisyChain():
            clients = server.grabOtherComputers()["hosts"]
            permaClients = pytools.IO.getJson(".\\permaclients.json")
            if permaClients["primary"] in clients:
                try:
                    clients.remove(permaClients["primary"])
                except:
                    pass
                try:
                    for ignoreClient in permaClients["ignore"]:
                        if ignoreClient in clients:
                            clients.remove(ignoreClient)
                except:
                    pass
                # sortedClients = sorted(clients, key = lambda s: sum(map(ord, s[1])), reverse=False)
                sortedClients = clients
                try:
                    sortedClients.remove("0.0.0.0")
                except:
                    pass
                sortedClients.append(permaClients["primary"])
            else:
                try:
                    clients.remove("0.0.0.0")
                except:
                    pass
                sortedClients = clients
            selfIndex = 0
            while selfIndex < len(sortedClients):
                if sortedClients[selfIndex] == server.interface:
                    break
                selfIndex = selfIndex + 1
            try:
                if selfIndex == (len(sortedClients) - 1):
                    nextClient = "localhost"
                else:
                    nextClient = "localhost"
            except:
                nextClient = server.hostname
            if selfIndex == 0:
                previousClient = False
            else:
                previousClient = sortedClients[-1]
            return [previousClient, nextClient]
        
        def setValues():
            clients = configure.vban.getDaisyChain()
            
            if clients[0] != False:
                if clients[0] != "0.0.0.0":
                    if str(globals.instance.get("vban.instream[0].ip", string=True)) != str(clients[0]):
                        globals.instance.set("vban.instream[0].name", "StreamClock")
                        globals.instance.set("vban.instream[0].ip", clients[0])
                        globals.instance.set("vban.instream[0].port", 6980)
                        globals.instance.set("vban.instream[0].route", 5)
                        globals.instance.set("vban.instream[0].on", 1)
                    
                    if globals.instance.get("vban.instream[1].ip", string=True) != clients[0]:
                        globals.instance.set("vban.instream[1].name", "StreamFireplace")
                        globals.instance.set("vban.instream[1].ip", clients[0])
                        globals.instance.set("vban.instream[1].port", 6980)
                        globals.instance.set("vban.instream[1].route", 6)
                        globals.instance.set("vban.instream[1].on", 1)
                        
                    if globals.instance.get("vban.instream[2].ip", string=True) != clients[0]:
                        globals.instance.set("vban.instream[2].name", "StreamWindow")
                        globals.instance.set("vban.instream[2].ip", clients[0])
                        globals.instance.set("vban.instream[2].port", 6980)
                        globals.instance.set("vban.instream[2].route", 7)
                        globals.instance.set("vban.instream[2].on", 1)
                    
                    if globals.instance.get("vban.instream[3].ip", string=True) != clients[0]:
                        globals.instance.set("vban.instream[3].name", "StreamOutside")
                        globals.instance.set("vban.instream[3].ip", clients[0])
                        globals.instance.set("vban.instream[3].port", 6980)
                        globals.instance.set("vban.instream[3].route", 0)
                        globals.instance.set("vban.instream[3].on", 1)
                    
                    if globals.instance.get("vban.instream[4].ip", string=True) != clients[0]:
                        globals.instance.set("vban.instream[4].name", "StreamPorch")
                        globals.instance.set("vban.instream[4].ip", clients[0])
                        globals.instance.set("vban.instream[4].port", 6980)
                        globals.instance.set("vban.instream[4].route", 1)
                        globals.instance.set("vban.instream[4].on", 1)
                    
                    if globals.instance.get("vban.instream[5].ip", string=True) != clients[0]:
                        globals.instance.set("vban.instream[5].name", "StreamGeneric")
                        globals.instance.set("vban.instream[5].ip", clients[0])
                        globals.instance.set("vban.instream[5].port", 6980)
                        globals.instance.set("vban.instream[5].route", 2)
                        globals.instance.set("vban.instream[5].on", 1)
                    
                    if globals.instance.get("vban.instream[6].ip", string=True) != clients[0]:
                        globals.instance.set("vban.instream[6].name", "StreamLight")
                        globals.instance.set("vban.instream[6].ip", clients[0])
                        globals.instance.set("vban.instream[6].port", 6980)
                        globals.instance.set("vban.instream[6].route", 3)
                        globals.instance.set("vban.instream[6].on", 1)
            
            if (clients[1] != False) and (clients[1] != "localhost"):
                if globals.instance.get("vban.outstream[0].ip", string=True) != clients[1]:
                    globals.instance.set("vban.outstream[0].name", "StreamClock")
                    globals.instance.set("vban.outstream[0].ip", clients[1])
                    globals.instance.set("vban.outstream[0].port", 6980)
                    globals.instance.set("vban.outstream[0].route", 1)
                    globals.instance.set("vban.outstream[0].channel", 8)
                    globals.instance.set("vban.outstream[0].on", 1)
                
                if globals.instance.get("vban.outstream[1].ip", string=True) != clients[1]:
                    globals.instance.set("vban.outstream[1].name", "StreamFireplace")
                    globals.instance.set("vban.outstream[1].ip", clients[1])
                    globals.instance.set("vban.outstream[1].port", 6980)
                    globals.instance.set("vban.outstream[1].route", 2)
                    globals.instance.set("vban.outstream[1].channel", 8)
                    globals.instance.set("vban.outstream[1].on", 1)
                
                if globals.instance.get("vban.outstream[2].ip", string=True) != clients[1]:
                    globals.instance.set("vban.outstream[2].name", "StreamWindow")
                    globals.instance.set("vban.outstream[2].ip", clients[1])
                    globals.instance.set("vban.outstream[2].port", 6980)
                    globals.instance.set("vban.outstream[2].route", 3)
                    globals.instance.set("vban.outstream[2].channel", 8)
                    globals.instance.set("vban.outstream[2].on", 1)
                
                if globals.instance.get("vban.outstream[3].ip", string=True) != clients[1]:
                    globals.instance.set("vban.outstream[3].name", "StreamOutside")
                    globals.instance.set("vban.outstream[3].ip", clients[1])
                    globals.instance.set("vban.outstream[3].port", 6980)
                    globals.instance.set("vban.outstream[3].route", 4)
                    globals.instance.set("vban.outstream[3].on", 1)
                
                if globals.instance.get("vban.outstream[4].ip", string=True) != clients[1]:
                    globals.instance.set("vban.outstream[4].name", "StreamPorch")
                    globals.instance.set("vban.outstream[4].ip", clients[1])
                    globals.instance.set("vban.outstream[4].port", 6980)
                    globals.instance.set("vban.outstream[4].route", 5)
                    globals.instance.set("vban.outstream[4].on", 1)
                
                if globals.instance.get("vban.outstream[5].ip", string=True) != clients[1]:
                    globals.instance.set("vban.outstream[5].name", "StreamGeneric")
                    globals.instance.set("vban.outstream[5].ip", clients[1])
                    globals.instance.set("vban.outstream[5].port", 6980)
                    globals.instance.set("vban.outstream[5].route", 6)
                    globals.instance.set("vban.outstream[5].on", 1)
                
                if globals.instance.get("vban.outstream[6].ip", string=True) != clients[1]:
                    globals.instance.set("vban.outstream[6].name", "StreamLight")
                    globals.instance.set("vban.outstream[6].ip", clients[1])
                    globals.instance.set("vban.outstream[6].port", 6980)
                    globals.instance.set("vban.outstream[6].route", 7)
                    globals.instance.set("vban.outstream[6].on", 1)
            
            return 
            
            if globals.instance.get("vban.Enable") != 1:
                globals.instance.set("vban.Enable", 1)
                
            configure.vban.clientsOld = clients
    
    outsideVolume = -30.0
    outsideLimiter = -14.0
    porchVolume = -30.0
    porchLimiter = -14.0
               
    def getOutsideVolumeBeforeHalloween(dateArray=False):
        
        if not dateArray:
            dateArray = pytools.clock.getDateTime()
        
        dayOfYear = (pytools.clock.dateArrayToUTC(dateArray) - pytools.clock.dateArrayToUTC([2023, 1, 1, 0, 0, 0])) / 60 / 60 / 24
        return 0.100629 * dayOfYear - 50.5912
    
    def getOutsideVolumeAfterHalloween():
        # For second function: https://www.desmos.com/calculator/hj309myssw
        dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([2023, 1, 1, 0, 0, 0])) / 60 / 60 / 24
        return ((0.00547945 / 1.650000) * dayOfYear - 21.258) + (7.02591 ** ( - 1.64709 * dayOfYear + 500.001) - 0.0000162749)
    
    def getLimiterModifierOnHalloween():
        
        try:
            dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
            halloweenOfYear = (pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 10, 31, 0, 0, 0]) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
            
            x = (dayOfYear - halloweenOfYear) * 24
            
            a = 3.1061
            b = 0.292463
            c = -0.923161
            d = -0.0000066956
            e = 2.71828182846
            f = -80.5216
            g = 16.7116
            
            out = a ** (b * (x + c)) + d * e ** ((((x - f) ** (2)) / (2 * g ** (2))))

            if out > 0:
                return out
            else:
                return 0
        except OverflowError:
            return 0
        except:
            print(traceback.format_exc())
            return 0
        
    def getLimiterModifierOnDayBeforeHalloween():
        
        try:
            dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
            halloweenOfYear = (pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 10, 30, 0, 0, 0]) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
            
            x = (dayOfYear - halloweenOfYear) * 24
            
            a = 3.1061
            b = 0.292463
            c = -0.923161
            d = -0.0000066956
            e = 2.71828182846
            f = -80.5216
            g = 16.7116
            
            out = a ** (b * (x + c)) + d * e ** ((((x - f) ** (2)) / (2 * g ** (2))))

            if out > 0:
                return out / 2
            else:
                return 0
        except OverflowError:
            return 0
        except:
            print(traceback.format_exc())
            return 0
        
    def getLimiterModifierOnDay(setDay, modifier=1):
        
        try:
            dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
            halloweenOfYear = (pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 10, 31, 0, 0, 0]) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
            
            x = ((dayOfYear - halloweenOfYear) + (304 - setDay)) * 24
            
            a = 3.1061
            b = 0.292463
            c = -0.923161
            d = -0.0000066956
            e = 2.71828182846
            f = -80.5216
            g = 16.7116
            
            out = a ** (b * (x + c)) + d * e ** ((((x - f) ** (2)) / (2 * g ** (2))))

            if out > 0:
                return out * modifier
            else:
                return 0
        except OverflowError:
            return 0
        except:
            print(traceback.format_exc())
            return 0
    
    def grabWeatherData():
        try:
            dataArray = pytools.IO.getList(".\\working\\dataList.pyl")[1]
            lightningDanger = pytools.IO.getJson(".\\working\\lightningData.json")["dangerLevel"]
            return [dataArray, lightningDanger]
        except:
            return False
    
    def getOutsideVolumeWeatherModifier(prevVal):
        
        dataf = configure.grabWeatherData()
        
        if dataf:
            lightningModif = (1.14898 ** (0.997531 * (dataf[1] + 0.00708756)) - 0.000982331) * 2
            windGustModif = (1.0382 ** (0.9993 * (dataf[0][0][1] - 1.00002)) - 0.963234) * 1.5
            windSpeedModif = 1.0382 ** (0.9993 * (dataf[0][0][0] - 1.00002)) - 0.963234
            if windGustModif > windSpeedModif:
                windModif = windGustModif
            else:
                windModif = windSpeedModif
            weatherModif = 0
            if dataf[0][0][4] == "mist":
                weatherModif = 1.2
            elif dataf[0][0][4] == "lightrain":
                weatherModif = 1.5
            elif dataf[0][0][4] == "rain":
                weatherModif = 3
            elif dataf[0][0][4] == "snow":
                weatherModif = 3
            elif dataf[0][0][4] == "thunder":
                weatherModif = 4.5
        else:
            lightningModif = 0
            windModif = 0
            weatherModif = 0
        
        modif = lightningModif + windModif + weatherModif
            
        dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([2023, 1, 1, 0, 0, 0])) / 60 / 60 / 24
         
        if dayOfYear < 304:
            adderDivider = (((123 + 181 - dayOfYear) / 123) * 0.8) + 1
        else:
            adderDivider = 1
            
        adderModif = prevVal + 20
        
        if adderModif < 1:
            adderModif = 1
        
        try:
            return prevVal + ((((-20 - prevVal) * (modif / 13.1)) + (modif / adderDivider)) / adderModif)
        except:
            return prevVal + ((((-20 - prevVal) * (modif / 13.1)) + (modif / adderDivider)) / 1)
    
    def getIsHoliday():
        isHalloween = ((pytools.clock.getDateTime()[1] == 10) and (pytools.clock.getDateTime()[2] == 31) and (pytools.clock.getDateTime()[3] > 6)) or ((pytools.clock.getDateTime()[1] == 11) and (pytools.clock.getDateTime()[2] == 1) and (pytools.clock.getDateTime()[2] < 6))
        isChristmas = (pytools.clock.getDateTime()[1] == 12) and ((pytools.clock.getDateTime()[2] == 25) or (pytools.clock.getDateTime()[2] == 24))
        return isHalloween or isChristmas
    
    def getIsWeekend():
        return (pytools.datetime.isoweekday(pytools.datetime(*pytools.clock.getDateTime())) == 7) or (pytools.datetime.isoweekday(pytools.datetime(*pytools.clock.getDateTime())) == 6) or ((pytools.datetime.isoweekday(pytools.datetime(*pytools.clock.getDateTime())) == 5) and (pytools.clock.getDateTime()[3] > 12))
    
    def getTimeModifier(prevVal, isLimiter=False, isPorch=False, noTime=False):
        if not noTime:
            if configure.getIsHoliday():
                if 7 < pytools.clock.getDateTime()[3] < 22:
                    percent = 0
                elif pytools.clock.getDateTime()[3] == 7:
                    percent = (1 - (((pytools.clock.getDateTime()[4] * 60) + pytools.clock.getDateTime()[5]) / 3600)) ** 2
                elif pytools.clock.getDateTime()[3] == 22:
                    percent = ((((pytools.clock.getDateTime()[4] * 60) + pytools.clock.getDateTime()[5]) / 3600) ** 2) / 5
                elif pytools.clock.getDateTime()[3] > 22:
                    percent = 0.2
                elif pytools.clock.getDateTime()[3] == 0:
                     percent = (((((pytools.clock.getDateTime()[4] * 60) + pytools.clock.getDateTime()[5]) / 3600) ** 2)) + 0.2
                     if percent > 1:
                        percent = 1
                else:
                    percent = 1
            elif configure.getIsWeekend():
                if 8 < pytools.clock.getDateTime()[3] < 21:
                    percent = 0
                elif pytools.clock.getDateTime()[3] == 8:
                    percent = (1 - (((pytools.clock.getDateTime()[4] * 60) + pytools.clock.getDateTime()[5]) / 3600)) ** 2
                elif pytools.clock.getDateTime()[3] == 21:
                    percent = (((pytools.clock.getDateTime()[4] * 60) + pytools.clock.getDateTime()[5]) / 3600) ** 2
                else:
                    percent = 1
            else:
                if 10 < pytools.clock.getDateTime()[3] < 19:
                    percent = 0
                elif pytools.clock.getDateTime()[3] == 10:
                    percent = (1 - (((pytools.clock.getDateTime()[4] * 60) + pytools.clock.getDateTime()[5]) / 3600)) ** 2
                elif pytools.clock.getDateTime()[3] == 19:
                    percent = (((pytools.clock.getDateTime()[4] * 60) + pytools.clock.getDateTime()[5]) / 3600) ** 2
                else:
                    percent = 1
                
                if percent < 0.1:
                    percent = 0.1
        else:
            percent = 0
        
        
        if isPorch:
            if (not isLimiter) and (percent > 0.3):
                percent = 0.3
            elif isLimiter:
                percent = percent * -0.15
        
        if not isLimiter:
            return (prevVal - (60 * percent))
        else:
            return prevVal - (28 * percent)
    
    def getOutsideVolumeOnHoliday(peakDateArray, peakModif=1, afterHour=False, timeScaleModif=1):
        # https://www.desmos.com/calculator/esomopbiwk
        dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
        peakDayOfYear = (pytools.clock.dateArrayToUTC(peakDateArray) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
        if afterHour:
            if dayOfYear > peakDayOfYear:
                if (dayOfYear <= (peakDayOfYear + 0.041666666666666664)):
                    return ((5 * 2 ** ( - (2 / timeScaleModif) * (dayOfYear - peakDayOfYear) ** (2))) * (1 - ((dayOfYear - peakDayOfYear) / 0.041666666666666664))) / peakModif
                else:
                    return 0
            else:
                return (5 * 2 ** ( - (2 / timeScaleModif) * (dayOfYear - peakDayOfYear) ** (2))) / (peakModif * 6)
        else:
            return (5 * 2 ** ( - (2 / timeScaleModif) * (dayOfYear - peakDayOfYear) ** (2))) / (peakModif * 6)
    
    def getOutsideVolume(isPorch=False, noTime=False):
        dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([2023, 1, 1, 0, 0, 0])) / 60 / 60 / 24
        actualDayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
        
        customModif = 0
        if not isPorch:
            customModif = configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 17, 23, 59, 59], peakModif=0.04, timeScaleModif=0.25)
            customModif = customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 18, 23, 59, 59], peakModif=0.1, timeScaleModif=0.25)
            customModif = customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 19, 23, 59, 59], peakModif=0.1, timeScaleModif=0.25)
            customModif = customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 20, 23, 59, 59], peakModif=0.093, timeScaleModif=0.25)
            customModif = customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 26, 23, 59, 59], peakModif=0.083, timeScaleModif=0.25)
            customModif = customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 27, 23, 59, 59], peakModif=0.08, timeScaleModif=0.25)
            customModif = customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 30, 12, 0, 0], peakModif=0.06)
        
        if dayOfYear > 304:
            if dayOfYear > 304.0208333333333:
                if configure.getOutsideVolumeAfterHalloween() <= -19:
                    return configure.getTimeModifier(configure.getOutsideVolumeWeatherModifier(configure.getOutsideVolumeAfterHalloween() + customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=0.06, afterHour=True) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=22) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=7.5)), noTime=noTime, isPorch=isPorch)
                else:
                    return configure.getTimeModifier(configure.getOutsideVolumeWeatherModifier(-19 + customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=0.06) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=22) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=7.5)), noTime=noTime, isPorch=isPorch)
            else:
                if configure.getOutsideVolumeAfterHalloween() <= -19:
                    newValue = configure.getOutsideVolumeWeatherModifier(configure.getOutsideVolumeAfterHalloween() + customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=0.06, afterHour=True) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=22) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=7.5))
                else:
                    newValue = configure.getOutsideVolumeWeatherModifier(-19 + customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=0.06) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=22) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=7.5))
                oldValue = configure.getOutsideVolumeWeatherModifier(configure.getOutsideVolumeBeforeHalloween(dateArray=[2023, 11, 1, 0, 0, 0]) + customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=0.06) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=1.5) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=2.5)) 
        
                percentage = (304.0208333333333 - dayOfYear) / 0.0208333333333
                return configure.getTimeModifier((oldValue * (percentage)) + (newValue * (1 - percentage)), noTime=noTime, isPorch=isPorch)
        else:
            return configure.getTimeModifier(configure.getOutsideVolumeWeatherModifier(configure.getOutsideVolumeBeforeHalloween() + customModif + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=0.6) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=1.5) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=2.5)), noTime=noTime, isPorch=isPorch)
    
    def getOutsideLimiter(volume, isPorch=False):
        # https://www.desmos.com/calculator/hgfrmpjpqs
        
        dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([2023, 1, 1, 0, 0, 0])) / 60 / 60 / 24
        
        a = 284.855
        b = -1
        c = 1.33358
        d = 36.3134
        g = -0.00000266904
        i = 0.281673
        j = 25.4979
        k = 0.00987916
        
        x = volume
        
        l = 0.180879
        m = -0.00532299
        o = 9.25592
        p = 6.62516
        
        if dayOfYear < 304:
            y = - l ** (m * (dayOfYear - o)) + p
        else:
            y = -8
        
        if volume > -20:
            y = -(-y + (y * ((volume + 20) / 5)))
        elif volume > -25:
            y = y * ((volume + 25) / 5)
        else:
            y = 0
        
        import math
        
        lim = (a * x ** (b) + (c * x) + d - (g * x ** (4) * math.sin((i * x) - j) + k)) + y
        
        tempModifier = configure.getLimiterModifierOnDay(300, modifier=0.1)
        tempModifier = tempModifier + configure.getLimiterModifierOnDay(299, modifier=0.1)
        tempModifier = tempModifier + configure.getLimiterModifierOnDay(293, modifier=0.05)
        tempModifier = tempModifier + configure.getLimiterModifierOnDay(292, modifier=0.025)
        tempModifier = tempModifier + configure.getLimiterModifierOnDay(290, modifier=0.025)
        tempModifier = tempModifier + configure.getLimiterModifierOnDay(303, modifier=0.025)
        lim = lim + configure.getLimiterModifierOnHalloween() + configure.getLimiterModifierOnDayBeforeHalloween() + tempModifier
        
        if lim > 0:
            lim = 0.0
        
        if (lim < 0) and (lim > -9):
            return configure.getTimeModifier((-math.fabs(lim) ** (math.fabs(lim / -9) ** 4)) / 1.1, isLimiter=True, isPorch=isPorch)
        else:
            return configure.getTimeModifier(lim / 1.1, isLimiter=True, isPorch=isPorch)
    
    def setOutsideVolume():
        configure.outsideVolume = configure.getOutsideVolume()
        configure.porchVolume = configure.getOutsideVolume(isPorch=True)
        configure.outsideLimiter = configure.getOutsideLimiter(configure.getOutsideVolume(noTime=True))
        configure.porchLimiter = configure.getOutsideLimiter(configure.getOutsideVolume(noTime=True), isPorch=True)
        globals.instance.set("Strip[0].Limit", configure.outsideLimiter)
        globals.instance.set("Strip[1].Limit", configure.porchLimiter)
        globals.instance.set("Strip[1].Gain", -13 + (configure.porchVolume - configure.outsideVolume))
        globals.instance.set("Bus[0].Gain", configure.outsideVolume)
        pytools.IO.saveJson("outsideProperties.json", {
            "volume": configure.outsideVolume,
            "limiter": configure.outsideLimiter
        })
        
        outputs = {
            "clock": globals.instance.get("Bus[1].device.name", string=True),
            "fireplace": globals.instance.get("Bus[2].device.name", string=True),
            "window": globals.instance.get("Bus[3].device.name", string=True),
            "outside": globals.instance.get("Bus[4].device.name", string=True)
        }
        pytools.IO.saveJson("serverOutputs.json", outputs)
    
    def handler():
        while True:
            try:
                configure.vban.setValues()
                configure.setOutsideVolume()
                time.sleep(1 + (2 * random.random()))
            except:
                print(traceback.format_exc())
                time.sleep(1)

class streams:
    
    lastUpdated = time.time()

    def handler():
        clients = configure.vban.getDaisyChain()
        clientsOld = clients

        streamClock = vban.speaker("clock", clients[0])
        streamFireplace = vban.speaker("fireplace", clients[0])
        streamWindow = vban.speaker("window", clients[0])
        streamOutside = vban.speaker("outside", clients[0])
        streamPorch = vban.speaker("porch", clients[0])
        streamGeneric = vban.speaker("generic", clients[0])
        streamLight = vban.speaker("light", clients[0])
        
        streamClock.run()
        streamFireplace.run()
        streamWindow.run()
        streamOutside.run()
        streamPorch.run()
        streamGeneric.run()
        streamLight.run()

        exitf = False

        lastUpdatedOld = streams.lastUpdated

        while not exitf:

            try:
                types = {}
                for thread in vban.pyvban.utils.receiver.allf.receiverUUIDs:
                    try:
                        types[vban.pyvban.utils.receiver.allf.receiverUUIDs[thread][2]._stream_name] 
                    except:
                        types[vban.pyvban.utils.receiver.allf.receiverUUIDs[thread][2]._stream_name] = []
                    types[vban.pyvban.utils.receiver.allf.receiverUUIDs[thread][2]._stream_name].append([thread, vban.pyvban.utils.receiver.allf.receiverUUIDs[thread]])
                
                for speaker in types:
                    loopCount = 0

                    inf = 0
                    toRemove = {}
                    for thread in types[speaker]:
                        if thread[1][2]._hasStopped:
                            vban.pyvban.utils.receiver.allf.receiverUUIDs.pop(thread[1][2]._uuid)
                            if not speaker in toRemove:
                                toRemove[speaker] = []
                            toRemove[speaker].append(inf)

                for speaker in toRemove:
                    for intf in toRemove[speaker]:
                        try:
                            types[speaker].pop(intf)
                        except:
                            print(traceback.format_exc())
                    
                    
                for speaker in types:
                    while (len(types[speaker]) > 1) and (loopCount < 100):
                        randomInt = random.randint(0, len(types[speaker]) - 1)
                        randomStream = types[speaker][randomInt][1]
                        loopCount = 0
                        while (not randomStream[2]._hasStopped) and (loopCount < 100):
                            try:
                                print("Stopping thread with uuid of " + str(types[speaker][randomInt][0]))
                                randomStream[2].stop()
                            except:
                                pass
                            loopCount = loopCount + 1
                            time.sleep(0.1)
                        
                        try:
                            if (loopCount < 100) or ((randomStream[2].lastStreamActivityTimestamp + 40) < time.time()):
                                types[speaker].pop(randomInt)
                                vban.pyvban.utils.receiver.allf.receiverUUIDs.pop(randomStream[2]._uuid)
                        except:
                            print(traceback.format_exc())

                outJson = {}
                for speaker in types:
                    for thread in types[speaker]:
                        if not speaker in outJson:
                            outJson[speaker] = []
                        outJson[speaker].append([thread[0], thread[1][0], thread[1][1], thread[1][3]])
                
                pytools.IO.saveJson("streamThreads.json", {
                    "speakers": outJson,
                    "error": False
                })
            except:
                exc = traceback.format_exc()
                print(exc)
                pytools.IO.saveJson("streamThreads.json", {
                    "speakers": {},
                    "error": exc
                })

            try:
                clients = configure.vban.getDaisyChain()
            
                if (clientsOld != clients):

                    print("Updated clients detected...")

                    streamClock.setReceiveFromIp(clients[0])
                    
                    streamFireplace.setReceiveFromIp(clients[0])

                    streamWindow.setReceiveFromIp(clients[0])
                    
                    streamOutside.setReceiveFromIp(clients[0])
                    
                    streamPorch.setReceiveFromIp(clients[0])
                    
                    streamGeneric.setReceiveFromIp(clients[0])
                    
                    streamLight.setReceiveFromIp(clients[0])

                    clientsOld = clients
            except:
                print(traceback.format_exc())

            try:
                def _streamWatchDog(streamf: vban.speaker):
                    try:
                        if ((streamf.lastUpdated + 120) < time.time()):
                            print("Stream watchdog detected crashed stream of type " + str(streamf.speakerType) + ". Restarting...")
                            streamf.exitf = True

                            try:
                                while not streamf.isRunning:
                                    streamf.exitf = True
                                    print("    > Waiting for stream of type " + str(streamf.speakerType) + " to exit...")
                                    time.sleep(0.1)
                            except:
                                pass

                            streamNew = vban.speaker(streamf.speakerType, streamf.receiveFrom)
                            streamNew.run()
                            return streamNew
                    except:
                        print(traceback.format_exc())
                    return streamf

                streamClock = _streamWatchDog(streamClock)
                streamFireplace = _streamWatchDog(streamFireplace)
                streamWindow = _streamWatchDog(streamWindow)
                streamOutside = _streamWatchDog(streamOutside)
                streamPorch = _streamWatchDog(streamPorch)
                streamGeneric = _streamWatchDog(streamGeneric)
                streamLight = _streamWatchDog(streamLight)

            except:
                print(traceback.format_exc())

            try:
                if streams.lastUpdated != lastUpdatedOld:
                    exitf = True
                
                streams.lastUpdated = time.time()
                pytools.IO.saveFile(".\\lastStreamsLoop.cx", str(time.time()))
                lastUpdatedOld = copy.deepcopy(streams.lastUpdated)
            except:
                print(traceback.format_exc())

            time.sleep(1)
            print("Handler looping...")

        print("Handler has exited.")
        streamClock.exitf = True
        streamFireplace.exitf = True
        streamWindow.exitf = True
        streamOutside.exitf = True
        streamPorch.exitf = True
        streamGeneric.exitf = True
        streamLight.exitf = True
        
        
if __name__ == '__main__':
    if sys.argv[1] == "--runStreams":
        try:
            if (float(pytools.IO.getFile("lastStreamsLoop.cx")) + 30) < time.time():
                streams.handler()
        except:
            streams.handler()