import modules.pytools as pytools
import modules.defferedTools as tools

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

import os
import sys
import time
import traceback
import threading

class client:
        
    def run():
        while True:
            if False:
                try:
                    for host in pytools.IO.getJson(".\\hosts.json")["hosts"]:
                        time.sleep(1)
                        try:
                            if pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                                "command": "ping"
                            })), timeout=5)["status"] == "success":
                                print("Host " + host + " still active.")
                                time.sleep(15)
                            try:
                                print("Host went offline. Removing host " + host + "...")
                                hostsFile = pytools.IO.getJson(".\\hosts.json")
                                while host in hostsFile["hosts"]:
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
                            try:
                                print("Host went offline. Removing host " + host + "...")
                                hostsFile = pytools.IO.getJson(".\\hosts.json")
                                while host in hostsFile["hosts"]:
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
            time.sleep(1)

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