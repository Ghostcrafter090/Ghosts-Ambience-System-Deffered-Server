import modules.pytools as pytools
import modules.defferedTools as tools
import vm

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

import os
import sys
import time
import traceback
import threading
import subprocess

try:
    from wakeonlan import send_magic_packet as wakeComputer
except:
    os.system("py -m pip install wakeonlan")

import modules.logManager as log

print = log.printLog

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
                        ips[interface].append([entryf[0], entryf[1]])
                except:
                    pass
        return ips

class client:
    
    hostsOrder = []
    
    neededHosts = 1
    
    def wakeOnLan():
        while True:
            try:
                files = os.listdir(".\\working")
                asleepHosts = []
                for file in files:
                    if file.find(".bl") != -1:
                        asleepHosts.append(file.split("host-")[1].split(".bl")[0])
                        print("Detecting asleep host file " + file + ".")
                asleepMacs = []
                for host in asleepHosts:
                    arpRequest = con.arp()
                    for interface in arpRequest:
                        for arpHost in arpRequest[interface]:
                            if arpHost[0] == host:
                                asleepMacs.append([arpHost[0], arpHost[1], interface])
                                print("Detecting asleep host file " + arpHost[0] + " with mac address " + arpHost[1] + " on interface " + interface + ".")
                for mac in asleepMacs:
                    print("Waking host " + mac[0] + " with mac address " + mac[1].replace("-", ".") + " on interface " + mac[2] + "...")
                    wakeComputer(mac[1].replace("-", "."), interface=mac[2])
                    time.sleep(120 / len(asleepMacs))
                    
                try:
                    load = puppet.getLoad()
                except:
                    load = False
                    print("No Sleep Clients Detected.")
                    time.sleep(30)
                if load:
                    if (load[1] / load[0]) < 0.35:
                        ticker = 0
                        while ((load[1] / load[0]) < 0.45) and (ticker < 1200):
                            try:
                                load = puppet.getLoad()
                            except:
                                pass
                            ticker = ticker + 5
                            time.sleep(5)
                    elif (load[1] / load[0]) < 0.45:
                        ticker = 0
                        while ((load[1] / load[0]) < 0.55) and (ticker < 600):
                            try:
                                load = puppet.getLoad()
                            except:
                                pass
                            ticker = ticker + 5
                            time.sleep(5)
                    elif (load[1] / load[0]) < 0.55:
                        ticker = 0
                        while ((load[1] / load[0]) < 0.65) and (ticker < 300):
                            try:
                                load = puppet.getLoad()
                            except:
                                pass
                            ticker = ticker + 5
                            time.sleep(5)
                    elif (load[1] / load[0]) < 0.65:
                        ticker = 0
                        while ((load[1] / load[0]) < 0.75) and (ticker < 150):
                            try:
                                load = puppet.getLoad()
                            except:
                                pass
                            ticker = ticker + 5
                            time.sleep(5)
            except:
                print(traceback.format_exc())
            time.sleep(1)
            
    def run():
        
        errorCounts = {}
        
        while True:
            try:
                for host in pytools.IO.getJson(".\\hosts.json")["hosts"]:
                    time.sleep(1)
                    try:
                        errorCounts[host]
                    except:
                        errorCounts[host] = 0
                    try:
                        if not os.path.exists(".\\working\\host-" + host + ".bm"):
                            if pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                                "command": "ping"
                            })), timeout=2)["status"] == "success":
                                print("Host " + host + " still active.")
                            else:
                                try:
                                    print("Host went offline. Removing host " + host + "...")
                                    hostsFile = pytools.IO.getJson(".\\hosts.json")
                                    while host in hostsFile["hosts"]:
                                        if not os.path.exists(".\\working\\host-" + host + ".bm"):
                                            hostsFile["hosts"].remove(host)
                                    hostsDataFile = pytools.IO.getJson(".\\working\\hostData.json")
                                    while host in hostsDataFile:
                                        hostsDataFile.pop(host)
                                    pytools.IO.saveJson(".\\hosts.json", hostsFile)
                                    pytools.IO.saveJson(".\\working\\hosts.json", hostsFile)
                                    pytools.IO.saveJson(".\\working\\hostData.json", hostsDataFile)
                                except:
                                    print("Hosts file not found or corrupted. Stack Trace: \n" + traceback.format_exc())
                        errorCounts[host] = 0
                    except:
                        errorCounts[host] = errorCounts[host] + 1
                        if errorCounts[host] > 2:
                            if not os.path.exists(".\\working\\host-" + host + ".bm"):
                                try:
                                    print("Host went offline. Removing host " + host + "...")
                                    hostsFile = pytools.IO.getJson(".\\hosts.json")
                                    while host in hostsFile["hosts"]:
                                        if not os.path.exists(".\\working\\host-" + host + ".bm"):
                                            hostsFile["hosts"].remove(host)
                                    hostsDataFile = pytools.IO.getJson(".\\working\\hostData.json")
                                    while host in hostsDataFile:
                                        hostsDataFile.pop(host)
                                    pytools.IO.saveJson(".\\hosts.json", hostsFile)
                                    pytools.IO.saveJson(".\\working\\hosts.json", hostsFile)
                                    pytools.IO.saveJson(".\\working\\hostData.json", hostsDataFile)
                                except:
                                    print("Hosts file not found or corrupted. Stack Trace: \n" + traceback.format_exc())
            except:
                print("Hosts file not found or corrupted. Stack Trace: \n" + traceback.format_exc())
            time.sleep(5)
            
    def sleepManager():
        while True:
            hostData = pytools.IO.getJson(".\\working\\hostData.json")
            max = 0
            current = 0
            for host in hostData:
                max = max + hostData[host]["max"]
                current = current + hostData[host]["current"]
            soundRatio = (current / max) * 100
            if soundRatio > 60:
                client.neededHosts = client.neededHosts + 1
            else:
                if client.neededHosts > 1:
                    client.neededHosts = client.neededHosts - 1
            time.sleep(300)
            
    def sendSleeps():
        while True:
            hostList =  pytools.IO.getJson(".\\hostData.json")
            hostArray = []
            for host in hostList:
                hostArray.append([host, hostList[host]["max"]])
            def doHostListSort(a):
                return a[1]
            sortedHostArray = sorted(hostArray, key=doHostListSort)
            i = 0
            blackHosts = []
            while i < client.neededHosts:
                blackHosts.append(sortedHostArray[i][0])
                i = i + 1
            pytools.IO.saveJson(".\\suspendedHosts.json", {
                "hosts": blackHosts
            })
            time.sleep(300)

class puppet:
    def ping(data):
        hosts = pytools.IO.getJson(".\\hosts.json")
        if str(hosts)[0] != "{":
            hosts = {
                "hosts": []
            }
        if data["ipAddress"] not in hosts["hosts"]:
            hosts["hosts"].append(data["ipAddress"])
            pytools.IO.saveJson(".\\hosts.json", hosts)
            pytools.IO.saveJson(".\\working\\hosts.json", hosts)
            client(data["ipAddress"]).thread.start()
    
    def getOthers():
        return pytools.IO.getJson('.\\hosts.json')["hosts"]
    
    def getLoad():
        hostData = pytools.IO.getJson('.\\working\\hostData.json')
        hostList = pytools.IO.getJson('.\\hosts.json')["hosts"]
        max = 0
        current = 0
        for host in hostList:
            max = max + hostData[host]["max"]
            current = current + hostData[host]["current"]
        if max == 0:
            if current == 0:
                return [10, 0]
        return [max, current]

class com:
    # Python 3 server example

    hostName = "0.0.0.0"
    serverPort = 5597
    
    webServer = False
    
    # Structure
    # ---------
    # {
    #     "command": "<command>"
    #     "data": {}
    # }
    
    class httpCommands:
        def _Get(request):
            jsonRequest = urllib.parse.parse_qs(urllib.parse.unquote_plus(request))
            print(jsonRequest)
            return json.loads(jsonRequest["/?json"][0])
            # print("\"" + jsonRequest + "\"")
            # return json.loads(jsonRequest)

    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                request = com.httpCommands._Get(self.path)
                if request["command"] == "getOtherComputers":
                    self.wfile.write(bytes(json.dumps({
                        "hosts": puppet.getOthers()
                    }), "utf-8"))
                if request["command"] == "ping":
                    try:
                        if request["data"]:
                            puppet.ping(request["data"])
                    except:
                        pass
                    self.wfile.write(bytes(json.dumps({
                        "status": "success"
                    }), "utf-8"))
                if request["command"] == "getLoad":
                    self.wfile.write(bytes(json.dumps({
                        "data": puppet.getLoad()
                    }), "utf-8"))
                if request["command"] == "getData":
                    dataToSend = {
                    }
                    for n in os.listdir(".\\working"):
                        if (n[-5:] == ".json"):
                            try:
                                dataToSend[n[:-5].lower().replace(".", "_").replace(" ", "_")]
                                try:
                                    dataToSend[n] = pytools.IO.getJson(".\\working\\" + n)
                                except:
                                    dataToSend[n] = False
                            except:
                                try:
                                    dataToSend[n[:-5].lower().replace(".", "_").replace(" ", "_")] = pytools.IO.getJson(".\\working\\" + n)
                                except:
                                    dataToSend[n[:-5].lower().replace(".", "_").replace(" ", "_")] = False
                        if (n[-4:] == ".pyl"):
                            try:
                                dataToSend[n[:-4].lower().replace(".", "_").replace(" ", "_")]
                                try:
                                    json.dumps({
                                        "test": pytools.IO.getList(".\\working\\" + n)[1]
                                    })
                                    dataToSend[n] = pytools.IO.getList(".\\working\\" + n)[1]
                                except:
                                    dataToSend[n] = False
                            except:
                                try:
                                    json.dumps({
                                        "test": pytools.IO.getList(".\\working\\" + n)[1]
                                    })
                                    dataToSend[n[:-4].lower().replace(".", "_").replace(" ", "_")] = pytools.IO.getList(".\\working\\" + n)[1]
                                except:
                                    dataToSend[n[:-4].lower().replace(".", "_").replace(" ", "_")] = False
                        if (n[-4:] == ".cxl"):
                            try:
                                dataToSend[n[:-4].lower().replace(".", "_").replace(" ", "_")]
                                try:
                                    dataToSend[n] = pytools.IO.getFile(".\\working\\" + n).split("\n")
                                except:
                                    dataToSend[n] = False
                            except:
                                try:
                                    dataToSend[n[:-4].lower().replace(".", "_").replace(" ", "_")] = pytools.IO.getFile(".\\working\\" + n).split("\n")
                                except:
                                    dataToSend[n[:-4].lower().replace(".", "_").replace(" ", "_")] = False
                    if (n[-3:] == ".cx"):
                        try:
                            dataToSend[n[:-3].lower().replace(".", "_").replace(" ", "_")]
                            try:
                                try:
                                    dataToSend[n] = float(pytools.IO.getFile(".\\working\\" + n))
                                except:
                                    dataToSend[n] = pytools.IO.getFile(".\\working\\" + n)
                            except:
                                dataToSend[n] = False
                        except:
                            try:
                                try:
                                    dataToSend[n[:-3].lower().replace(".", "_").replace(" ", "_")] = float(pytools.IO.getFile(".\\working\\" + n))
                                except:
                                    dataToSend[n[:-3].lower().replace(".", "_").replace(" ", "_")] = pytools.IO.getFile(".\\working\\" + n)
                            except:
                                dataToSend[n[:-3].lower().replace(".", "_").replace(" ", "_")] = False
                    self.wfile.write(bytes(json.dumps(dataToSend), "utf-8"))
                if request["command"] == "setBlackList":
                    pytools.IO.saveFile(".\\working\\host-" + str(self.client_address[0]) + ".bl", "")
                    self.wfile.write(bytes(json.dumps({
                        "status": "success"
                    }), "utf-8"))
                if request["command"] == "removeBlackList":
                    os.system("del \".\\working\\host-" + str(self.client_address[0]) + ".bl\" /f /q")
                    self.wfile.write(bytes(json.dumps({
                        "status": "success"
                    }), "utf-8"))
            except:
                self.send_error(400, traceback.format_exc())

    def start():
        com.webServer = HTTPServer((com.hostName, com.serverPort), com.MyServer)
        print("Server started http://%s:%s" % (com.hostName, com.serverPort))

        try:
            com.webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        com.webServer.server_close()
        print("Server stopped.")

    def run():
        threadVoicemeeter = threading.Thread(target=vm.vm.handler)
        threadVConfigure = threading.Thread(target=vm.configure.handler)
        threadWakeOnLan = threading.Thread(target=client.wakeOnLan)
        threadVoicemeeter.start()
        threadVConfigure.start()
        threadWakeOnLan.start()
        while True:
            threadf = threading.Thread(target=com.start)
            threadf.start()
            time.sleep(1)
            try:
                while pytools.net.getJsonAPI("http://localhost:5597?json=" + urllib.parse.quote(json.dumps({
                    "command": "ping"
                })), timeout=1)["status"] == "success":
                    time.sleep(15)
                threadf = threading.Thread(target=com.start)
                threadf.start()
                time.sleep(1)
            except:
                threadf = threading.Thread(target=com.start)
                threadf.start()
                time.sleep(1)

class hosts:
    hostList = []

def main():
    clientManager = threading.Thread(target=client.run)
    clientManager.start()
    pytools.IO.saveFile(".\\working\\server.derp", "derp")
    if os.path.exists(".\\serverCommands.json") == False:
        pytools.IO.saveJson(".\\serverCommands.json", {
            "commands": [],
            "execute": 0
        })
    print("Server started.")
    while True:
        try:
            commands = pytools.IO.getJson(".\\serverCommands.json")
            if commands["execute"] == 1:
                for command in commands["commands"]:
                    print("running command: " + command)
                    os.system("start /min "" py console.py " + command + " --server")
                commands["execute"] = 0
                pytools.IO.saveJson(".\\serverCommands.json", commands)
        except:
            pass
        time.sleep(1)
        if (pytools.clock.getDateTime()[5] % 30) == 0:
            try:
                if not os.path.exists("noUpdateTime.derp"):
                    os.system("net start w32time")
                    os.system("w32tm /resync")
            except:
                pass
        
try:
    for n in sys.argv:
        if n == "--run":
            threading.Thread(target=main).start()
            threading.Thread(target=com.run).start()
except:
    pass