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

import modules.logManager as log

print = log.printLog

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
                clients.remove(permaClients["primary"])
                # sortedClients = sorted(clients, key = lambda s: sum(map(ord, s[1])), reverse=False)
                sortedClients = clients
                sortedClients.append(permaClients["primary"])
            else:
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
                if globals.instance.get("vban.instream[0].ip", string=True) != clients[0]:
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
            
            if clients[1] != False:
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
                
            if globals.instance.get("vban.Enable") != 1:
                globals.instance.set("vban.Enable", 1)
                
            configure.vban.clientsOld = clients
    
    outsideVolume = -30.0
    outsideLimiter = -14.0
               
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
    
    def getOutsideVolumeOnHoliday(peakDateArray, peakModif=1, afterHour=False):
        # https://www.desmos.com/calculator/esomopbiwk
        dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
        peakDayOfYear = (pytools.clock.dateArrayToUTC(peakDateArray) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
        if afterHour:
            if dayOfYear > peakDayOfYear:
                if (dayOfYear <= (peakDayOfYear + 0.041666666666666664)):
                    return ((5 * 2 ** ( - 2 * (dayOfYear - peakDayOfYear) ** (2))) * (1 - ((dayOfYear - peakDayOfYear) / 0.041666666666666664))) / peakModif
                else:
                    return 0
            else:
                return (5 * 2 ** ( - 2 * (dayOfYear - peakDayOfYear) ** (2))) / (peakModif * 6)
        else:
            return (5 * 2 ** ( - 2 * (dayOfYear - peakDayOfYear) ** (2))) / (peakModif * 6)
    
    def getOutsideVolume():
        dayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([2023, 1, 1, 0, 0, 0])) / 60 / 60 / 24
        actualDayOfYear = (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) / 60 / 60 / 24
        if dayOfYear > 304:
            if dayOfYear > 304.0208333333333:
                if configure.getOutsideVolumeAfterHalloween() <= -19:
                    return configure.getOutsideVolumeWeatherModifier(configure.getOutsideVolumeAfterHalloween() + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=5.3, afterHour=True) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=22) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=7.5))
                else:
                    return configure.getOutsideVolumeWeatherModifier(-19 + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=5.3) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=22) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=7.5))
            else:
                if configure.getOutsideVolumeAfterHalloween() <= -19:
                    newValue = configure.getOutsideVolumeWeatherModifier(configure.getOutsideVolumeAfterHalloween() + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=5.3, afterHour=True) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=22) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=7.5))
                else:
                    newValue = configure.getOutsideVolumeWeatherModifier(-19 + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=5.3) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=22) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=7.5))
                oldValue = configure.getOutsideVolumeWeatherModifier(configure.getOutsideVolumeBeforeHalloween(dateArray=[2023, 11, 1, 0, 0, 0]) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=2.3) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=1.5) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=2.5)) 
        
                percentage = (304.0208333333333 - dayOfYear) / 0.0208333333333
                return (oldValue * (percentage)) + (newValue * (1 - percentage))
        else:
            return configure.getOutsideVolumeWeatherModifier(configure.getOutsideVolumeBeforeHalloween() + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 31, 23, 59, 59], peakModif=2.3) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 10, 13, 23, 59, 59], peakModif=1.5) + configure.getOutsideVolumeOnHoliday([pytools.clock.getDateTime()[0], 12, 24, 23, 59, 59], peakModif=2.5))
    
    def getOutsideLimiter(volume):
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
        
        lim = lim + configure.getLimiterModifierOnHalloween()
        
        if lim > 0:
            lim = 0.0
        
        if (lim < 0) and (lim > -9):
            return (-math.fabs(lim) ** (math.fabs(lim / -9) ** 4)) / 1.1
        else:
            return lim / 1.1
    
    def setOutsideVolume():
        configure.outsideVolume = configure.getOutsideVolume()
        configure.outsideLimiter = configure.getOutsideLimiter(configure.outsideVolume)
        globals.instance.set("Strip[0].Limit", configure.outsideLimiter)
        globals.instance.set("Strip[1].Limit", configure.outsideLimiter)
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