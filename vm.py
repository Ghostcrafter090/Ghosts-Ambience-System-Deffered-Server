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
            ips = {}
            for entry in ipsDirty:
                if entry.find("Interface:") != -1:
                    interface = entry.split("Interface: ")[1].split(" ")[0]
                    ips[interface] = []
                elif entry.find("Internet Address") != -1:
                    pass
                else:
                    try:
                        entryf = entry.split(" ")
                        while '' in entryf:
                            entryf.remove('')
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
                vm.checkStatus()
            except:
                pass
            time.sleep(1)
            

class configure:
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
                            "windown": [outFinal[1]["name"], "MME"],
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
                            "windown": [outFinal[1]["name"], "MME"],
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
                if globals.instance.inputs[1].device != configure.local.getInputs()["windown"][0]:
                    globals.instance.set("Strip[1].device.mme", configure.local.getInputs()["windown"][0])
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
            sortedClients = sorted(clients, key = lambda s: sum(map(ord, s[1])), reverse=False)
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
            
            if clients != configure.vban.clientsOld:
                
                configure.vban.clientsOld = clients
            
                if clients[0]:
                    globals.instance.set("vban.instream[0].name", "StreamClock")
                    globals.instance.set("vban.instream[0].ip", clients[0])
                    globals.instance.set("vban.instream[0].port", 6980)
                    globals.instance.set("vban.instream[0].route", 5)
                    globals.instance.set("vban.instream[0].on", 1)
                    
                    globals.instance.set("vban.instream[1].name", "StreamFireplace")
                    globals.instance.set("vban.instream[1].ip", clients[0])
                    globals.instance.set("vban.instream[1].port", 6980)
                    globals.instance.set("vban.instream[1].route", 6)
                    globals.instance.set("vban.instream[1].on", 1)
                    
                    globals.instance.set("vban.instream[2].name", "StreamWindow")
                    globals.instance.set("vban.instream[2].ip", clients[0])
                    globals.instance.set("vban.instream[2].port", 6980)
                    globals.instance.set("vban.instream[2].route", 7)
                    globals.instance.set("vban.instream[2].on", 1)
                    
                    globals.instance.set("vban.instream[3].name", "StreamOutside")
                    globals.instance.set("vban.instream[3].ip", clients[0])
                    globals.instance.set("vban.instream[3].port", 6980)
                    globals.instance.set("vban.instream[3].route", 0)
                    globals.instance.set("vban.instream[3].on", 1)
                    
                    globals.instance.set("vban.instream[4].name", "StreamWindown")
                    globals.instance.set("vban.instream[4].ip", clients[0])
                    globals.instance.set("vban.instream[4].port", 6980)
                    globals.instance.set("vban.instream[4].route", 1)
                    globals.instance.set("vban.instream[4].on", 1)
                    
                    globals.instance.set("vban.instream[5].name", "StreamGeneric")
                    globals.instance.set("vban.instream[5].ip", clients[0])
                    globals.instance.set("vban.instream[5].port", 6980)
                    globals.instance.set("vban.instream[5].route", 2)
                    globals.instance.set("vban.instream[5].on", 1)
                    
                    globals.instance.set("vban.instream[6].name", "StreamLight")
                    globals.instance.set("vban.instream[6].ip", clients[0])
                    globals.instance.set("vban.instream[6].port", 6980)
                    globals.instance.set("vban.instream[6].route", 3)
                    globals.instance.set("vban.instream[6].on", 1)
                
                globals.instance.set("vban.outstream[0].name", "StreamClock")
                globals.instance.set("vban.outstream[0].ip", clients[1])
                globals.instance.set("vban.outstream[0].port", 6980)
                globals.instance.set("vban.outstream[0].route", 1)
                globals.instance.set("vban.outstream[0].on", 1)
                
                globals.instance.set("vban.outstream[1].name", "StreamFireplace")
                globals.instance.set("vban.outstream[1].ip", clients[1])
                globals.instance.set("vban.outstream[1].port", 6980)
                globals.instance.set("vban.outstream[1].route", 2)
                globals.instance.set("vban.outstream[1].on", 1)
                
                globals.instance.set("vban.outstream[2].name", "StreamWindow")
                globals.instance.set("vban.outstream[2].ip", clients[1])
                globals.instance.set("vban.outstream[2].port", 6980)
                globals.instance.set("vban.outstream[2].route", 3)
                globals.instance.set("vban.outstream[2].on", 1)
                
                globals.instance.set("vban.outstream[3].name", "StreamOutside")
                globals.instance.set("vban.outstream[3].ip", clients[1])
                globals.instance.set("vban.outstream[3].port", 6980)
                globals.instance.set("vban.outstream[3].route", 4)
                globals.instance.set("vban.outstream[3].on", 1)
                
                globals.instance.set("vban.outstream[4].name", "StreamWindown")
                globals.instance.set("vban.outstream[4].ip", clients[1])
                globals.instance.set("vban.outstream[4].port", 6980)
                globals.instance.set("vban.outstream[4].route", 5)
                globals.instance.set("vban.outstream[4].on", 1)
                
                globals.instance.set("vban.outstream[5].name", "StreamGeneric")
                globals.instance.set("vban.outstream[5].ip", clients[1])
                globals.instance.set("vban.outstream[5].port", 6980)
                globals.instance.set("vban.outstream[5].route", 6)
                globals.instance.set("vban.outstream[5].on", 1)
                
                globals.instance.set("vban.outstream[6].name", "StreamLight")
                globals.instance.set("vban.outstream[6].ip", clients[1])
                globals.instance.set("vban.outstream[6].port", 6980)
                globals.instance.set("vban.outstream[6].route", 7)
                globals.instance.set("vban.outstream[6].on", 1)
                
                if globals.instance.get("vban.Enable") != 1:
                    globals.instance.set("vban.Enable", 1)
            
    def handler():
        while True:
            try:
                configure.vban.setValues()
                time.sleep(20)
            except:
                print(traceback.format_exc())
                time.sleep(1)