try:
    import modules.pytools as pytools
except:
    import pytools
from re import L
import time
import os
import trace
import termcolor
import sys
import threading
import ctypes
import msvcrt
import copy
import subprocess

import ephem
import datetime

import urllib.parse
import json
import random
import math

def getNewJson(path, doPrint=True):
    import traceback
    error = 0
    
    if path in globals.jsonDictionary:
        if (globals.jsonDictionary[path][1] + 1) > time.time():
            return globals.jsonDictionary[path][0]
    
    try:
        if path[0:2] == "\\\\":
            ifn = 0
            _doStop = False
            while (ifn < 2) and (not _doStop):
                try:
                    jsonData = pytools.net.getJsonAPI("http://" + flags.remote + ":" + str(random.randint(6000, 6029)) + "?json=" + urllib.parse.quote(json.dumps({
                        "command": "getJson",
                        "data": {
                            "path": ".\\" + path.split("\\ambience\\")[1]
                        }
                    })), timeout=1)["data"]
                    _doStop = True
                except:
                    ifn = ifn + 1
                
            if ifn >= 2:
                jsonData = pytools.net.getJsonAPI("http://" + flags.remote + ":" + str(random.randint(6000, 6029)) + "?json=" + urllib.parse.quote(json.dumps({
                        "command": "getJson",
                        "data": {
                            "path": ".\\" + path.split("\\ambience\\")[1]
                        }
                    })), timeout=1)["data"]
        else:
            file = open(path, "r")
            jsonData = json.loads(file.read())
            file.close()
    except:
        if doPrint:
            print(traceback.format_exc())
            print("Unexpected error:", sys.exc_info())
            print(path)
        error = 1
    if error != 0:
        jsonData = error
    globals.jsonDictionary[path] = [jsonData, time.time()]
    return jsonData

def getMultiFile(listf, doPrint=False):
    try:
        if str(listf) in globals.multifileDictionary:
            if (globals.multifileDictionary[str(listf)][1] + 2) > time.time():
                return globals.multifileDictionary[str(listf)][0]
        data = pytools.net.getJsonAPI("http://" + flags.remote + ":" + str(random.randint(6000, 6029)) + "?json=" + urllib.parse.quote(json.dumps({
            "command": "getMultiFile",
            "data": {
                "list": listf.values()
            }
        })))["data"]
        globals.multifileDictionary[str(listf)] = [data, time.time()]
        return data
    except:
        if doPrint:
            print(traceback.format_exc())
        return {}

def getMultiJson(listf, doPrint=False):
    try:
        return pytools.net.getJsonAPI("http://" + flags.remote + ":" + str(random.randint(6000, 6029)) + "?json=" + urllib.parse.quote(json.dumps({
            "command": "getMultiJson",
            "data": {
                "list": list(listf.values())
            }
        })))["data"]
    except:
        if doPrint:
            print(traceback.format_exc())
        return {}

def getNewFile(path, doPrint=True):
    import traceback
    error = 0
    try:
        if path[0:2] == "\\\\":
            jsonData = pytools.net.getJsonAPI("http://" + flags.remote + ":" + str(random.randint(6000, 6029)) + "?json=" + urllib.parse.quote(json.dumps({
                "command": "getFile",
                "data": {
                    "path": ".\\" + path.split("\\ambience\\")[1]
                }
            })))["data"]
        else:
            file = open(path, "r")
            jsonData = file.read()
            file.close()
    except:
        if doPrint:
            print("Unexpected error:", traceback.format_exc())
        error = 1
    if error != 0:
        jsonData = error
    return jsonData

pytools.IO.getFile = getNewFile
pytools.IO.getJson = getNewJson

import traceback

from ctypes import wintypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

os.system("color")

class flags:
    display = True
    exitf = False
    apiKey = ""
    pythonf = False
    remote = False
    defaultSystemState = False
    server = False
    timeout = 3000
    bypass = False
    unpack = True
    webMode = False
    restart = False
    displayOnScreen = True
    update = False
    enigma = False
    enigmaSettings = {
        "salt": 0,
        "rotors": 0,
        "plugboard": ""
    }
    monitor = False
    
class globals:
    maxY = 0
    lastSSTCGrabs = {}
    multifileDictionary = {}
    jsonDictionary = {}
    multijsonDictionary = {}
    
    lastServerGrab = 0
    serverData = {}
    
    hallowIndex = 0
    
    forecastLength = False
    
class tools:
    def max_window(lines=None):
        fd = os.open('CONOUT$', os.O_RDWR)
        try:
            hCon = msvcrt.get_osfhandle(fd)
            max_size = kernel32.GetLargestConsoleWindowSize(hCon)
            if max_size.X == 0 and max_size.Y == 0:
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            os.close(fd)
        cols = 200
        hWnd = kernel32.GetConsoleWindow()
        if cols and hWnd:
            if lines is None:
                globals.maxY = max_size.Y
            else:
                globals.maxY = max_size.Y
            subprocess.check_call('mode.com con cols={} lines={}'.format(cols, globals.maxY))
            user32.ShowWindow(hWnd, SW_MAXIMIZE)
            
    def getRemote():
        if flags.remote == False:
            return "localhost"
        else:
            return flags.remote
    
    def colorMult(colorA, colorB):
        colors = {
            "grey": [128, 128, 128],
            "red": [255, 0, 0],
            "green": [0, 192, 0],
            "blue": [0, 0, 255],
            "yellow": [255, 255, 0],
            "magenta": [255, 0, 255],
            "cyan": [64, 64, 255],
            "light_red": [255, 32, 32],
            "light_green": [32, 255, 32],
            "light_blue": [32, 32, 255],
            "light_yellow": [255, 255, 128],
            "light_magenta": [255, 32, 255],
            "light_cyan": [96, 96, 255],
            "black": [0, 0, 0],
            "white": [255, 255, 255]
        }
        
        newColor = []
        i = 0
        while i < 3:
            newColor.append(255 * ((colors[colorA][i] + colors[colorB][i]) / 510))
            i = i + 1
        
        _newColor = copy.deepcopy(newColor)
        
        newColor[0] = newColor[0] * (255 / max(_newColor))
        newColor[1] = newColor[1] * (255 / max(_newColor))
        newColor[2] = newColor[2] * (255 / max(_newColor))
        
        distances = []
        for color in colors:
            distances.append(math.fabs(newColor[0] - colors[color][0]) + math.fabs(newColor[1] - colors[color][1]) + math.fabs(newColor[2] - colors[color][2]))
        
        out = list(colors.keys())[distances.index(min(distances))]
        if (out == "white") or (out == colorA) or (out == colorB):
            distances = []
            for color in colors:
                distances.append(math.fabs(_newColor[0] - colors[color][0]) + math.fabs(_newColor[1] - colors[color][1]) + math.fabs(_newColor[2] - colors[color][2]))
                
            out = list(colors.keys())[distances.index(min(distances))]
        
        return out
        
    def getValueColor(x, typef="volume"):
        if typef == "speed":
            if x < 0.25:
                return "blue"
            if 0.25 < x < 0.65:
                return "light_blue"
            if 0.65 < x < 0.85:
                return "cyan"
            if 0.85 < x < 0.95:
                return "light_cyan"
            if 0.95 < x < 1.05:
                return "light_green"
            if 1.05 < x < 1.15:
                return "light_yellow"
            if 1.15 < x < 1.25:
                return "yellow"
            if 1.25 < x < 1.45:
                return "light_red"
            if 1.45 < x < 1.85:
                return "red"
            
            return "magenta"
        
        if x < 10:
            return "blue"
        if x < 20:
            return "light_blue"
        if x < 30:
            return "cyan"
        if x < 40:
            return "light_cyan"
        if x < 50:
            return "light_green"
        if x < 60:
            return "light_yellow"
        if x < 70:
            return "yellow"
        if x < 80:
            return "light_red"
        if x < 90:
            return "red"
        if x < 100:
            return "magenta"
        
        return "light_magenta"
    
    def getWeatherColor(value, typef="temperature"):
        
        if typef != "condition":
            newValue = ""
            for x in value:
                if x in "0123456789.-":
                    newValue = newValue + x
                    
            value = newValue
        else:
            newValue = ""
            for x in value:
                if x in "abcdefghijklmnopqrstuvwxyz":
                    newValue = newValue + x
                    
            value = newValue
        
        try:
            value = float(value)
        except:
            pass
        
        if typef == "wind":
            if value < 3:
                return "grey"
            if value < 3.43:
                return "blue"
            if value < 4.06:
                return "light_blue"
            if value < 4.96:
                return "cyan"
            if value < 6.31:
                return "light_cyan"
            if value < 8.41:
                return "light_green"
            if value < 11.87:
                return "light_yellow"
            if value < 22.97:
                return "yellow"
            if value < 29.53:
                return "light_red"
            if value < 50.59:
                return "red"
            
            return "magenta"
        
        if typef == "pressure":
            if value > 1050:
                return "grey"
            if value > 1040:
                return "blue"
            if value > 1030:
                return "light_blue"
            if value > 1020:
                return "cyan"
            if value > 1010:
                return "light_cyan"
            if value > 990:
                return "light_green"
            if value > 980:
                return "light_yellow"
            if value > 970:
                return "yellow"
            if value > 960:
                return "light_red"
            
            return "red"
        
        if typef == "rain":
            if value < 0.1:
                return "grey"
            if value < 0.2:
                return "blue"
            if value < 0.3:
                return "light_blue"
            if value < 0.4:
                return "cyan"
            if value < 0.5:
                return "light_cyan"
            if value < 0.6:
                return "light_green"
            if value < 0.7:
                return "light_yellow"
            if value < 0.8:
                return "yellow"
            if value < 0.9:
                return "light_red"
            
            return "red"
        
        if typef == "humidity":
            if value > 90:
                return "blue"
            if value > 80:
                return "light_blue"
            if value > 70:
                return "cyan"
            if value > 60:
                return "light_cyan"
            if value > 50:
                return "light_green"
            if value > 40:
                return "light_yellow"
            if value > 30:
                return "yellow"
            if value > 20:
                return "light_red"
            if value > 5:
                return "red"
            
            return "magenta"
        
        if typef == "lightning":
            if value < -81:
                return "grey"
            if value < -27:
                return "blue"
            if value < -9:
                return "light_blue"
            if value < -3:
                return "cyan"
            if value < -1:
                return "light_cyan"
            if value < 0:
                return "light_green"
            if value < 1:
                return "light_yellow"
            if value < 2:
                return "yellow"
            if value < 3:
                return "light_red"
            
            return "red"

        if typef == "condition":
            if value == "snow":
                return "cyan"
            if value == "mist":
                return "light_cyan"
            if value == "lightrain":
                return "light_blue"
            if value == "rain":
                return "blue"
            if value == "clouds":
                return "grey"
            if value == "clear":
                return "light_yellow"
            if value == "thunder":
                return "red"
            
            return "grey"
        
        if value < -21:
            return "magenta"
        if value < -20:
            return "blue"
        if value < -7:
            return "light_blue"
        if value < 0:
            return "cyan"
        if value < 7:
            return "light_cyan"
        if value < 14:
            return "light_green"
        if value < 21:
            return "light_yellow"
        if value < 28:
            return "yellow"
        if value < 35:
            return "light_red"
        
        return "red"

        
    def inputOption(text: str, type):
        errork = True
        while errork:
            try:
                salt = type(input(text))
                errork = False
            except:
                print("Value incorrect. Please enter a value of type " + type.__name__ + ".")
        return salt

class comm:
    def wait(timeout):
        n = 0
        try:
            executef = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", False)["execute"]
        except:
            executef = 0
        while (executef != 0) and (timeout > n):
            n = n + 1
            time.sleep(0.001)
            executef = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", False)["execute"]
        if timeout <= n:
            return False
        else:
            return True
    
    def sendStart():
        pytools.IO.saveJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", {
            "commands": [
                "--run --start --apiKey=" + flags.apiKey
            ],
            "execute": 1
        })
        return comm.wait(flags.timeout)
    
    def sendUpdate():
        if flags.unpack:
            pytools.IO.saveJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", {
                "commands": [
                    "--run --update"
                ],
                "execute": 1
            })
        else:
            pytools.IO.saveJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", {
                "commands": [
                    "--run --update --noUnpack"
                ],
                "execute": 1
            })
        return comm.wait(flags.timeout)
    
    def sendUpdateRestart():
        if flags.unpack:
            pytools.IO.saveJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", {
                "commands": [
                    "--run --stop --start --update --apiKey=" + flags.apiKey
                ],
                "execute": 1
            })
        else:
            pytools.IO.saveJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", {
                "commands": [
                    "--run --stop --start --update --noUnpack --apiKey=" + flags.apiKey
                ],
                "execute": 1
            })
        return comm.wait(flags.timeout)

    def sendStop():
        pytools.IO.saveJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", {
            "commands": [
                "--run --stop"
            ],
            "execute": 1
        })
        return comm.wait(flags.timeout)
    
    def ping():
        pytools.IO.saveJson("\\\\" + flags.remote + "\\ambience\\" + "serverCommands.json", {
            "commands": [
                "--run --ping"
            ],
            "execute": 1
        })
        print("Pinging...")
        return comm.wait(flags.timeout)
    
    enCount = 0
    
    def connect(enf=True):
        en = True
        errord = subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "ping " + flags.remote + " -w 1 -n 1")[0]
        if errord != 0:
            print("Could not connect to remote system. IP address " + flags.remote + "is not available.")
            en = False
        else:
            errord = subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "dir \\\\" + flags.remote + "\\ambience")[0]
            if errord != 0:
                print("Could not connect to remote system. Filesystem on IP address " + flags.remote + "doesn't exist or is not configured.")
                en = False
                comm.enCount = comm.enCount + 1
                if comm.enCount > 30:
                    flags.exitf = True
                    exit()
            else:
                os.chdir("\\\\" + flags.remote + "\\ambience")
                errord = comm.ping()
                if errord:
                    print("connected.")
                else:
                    print("Server not responding. Please check network connection, and check to make sure the remote ambience server is online.")
                    en = False
        return en and enf
    
class system:
    def start():
        if flags.remote == False:
            if flags.pythonf == False:
                if os.path.exists("C:\\windows\\py.exe"):
                    flags.pythonf = "C:\\windows\\py.exe"
            if flags.pythonf == False:
                for n in os.environ["path"].split(";"): 
                    if n.find("\\Python\\") != -1:
                        flags.pythonf = n
            if flags.pythonf == False:
                flags.pythonf = input("Please specify the folder containing the python executable: ")
            if flags.apiKey == "":
                flags.apiKey = input("Please specify apiKey: ")
            if flags.apiKey != "":
                if flags.pythonf[-4:] != ".exe":
                    subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "copy \"" + flags.pythonf + "python.exe\" \".\\ambience.exe\" /y")[0]
                    subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "copy \".\\ambience.exe\" \"" + flags.pythonf + "ambience.exe\" /y")[0]
                else:
                    subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "copy \"" + flags.pythonf + "\" \".\\ambience.exe\" /y")[0]
                    subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "copy \".\\ambience.exe\" \"" + flags.pythonf.replace("python.exe", "ambience.exe").replace("py.exe", "ambience.exe") + "\" /y")[0]
                os.system("start /min \"\" \".\\ambience.exe\" main.py --run --deffered --apiKey=" + flags.apiKey)
                system.status.active = True
        else:
            while comm.connect() == False:
                pass
            if comm.sendStart() == False:
                while comm.connect() == False:
                    pass
                if comm.sendStart() == False:
                    raise Exception("Connect error. Unable to communicate with remote ambience server")
                else:
                    system.status.active = True
            else:
                system.status.active = True
    
    def update(restart=False):
        if flags.remote == False:
            if restart:
                system.stop()
            noUpdate = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "noUpdate.json", False)
            print("reading noUpdate...")
            for n in noUpdate["list"]:
                fileName = n.split("\\")[-1]
                print(n)
                subprocess.getstatusoutput("xcopy \"" + n + "\" \"..\\ambience_py_updates\\" + n.split(fileName)[0] + "\" /i /e /c /y")[0]
            print("Pulling from repository...")
            print(subprocess.getoutput("git restore *"))
            print(subprocess.getoutput("git pull -f"))
            print("(This may take a while) Rerunning repo install...")
            if flags.unpack:
                subprocess.getstatusoutput("py setup.py --confirmInstall")
            print("Copying noUpdate files back to main repo.")
            subprocess.getstatusoutput("xcopy \"..\\ambience_py_updates\\*\" \".\" /e /c /y")
            if restart:
                system.start()
        else:
            while comm.connect() == False:
                pass
            if restart:
                if comm.sendUpdateRestart() == False:
                    while comm.connect() == False:
                        pass
                    if comm.sendUpdateRestart() == False:
                        raise Exception("Connect error. Unable to communicate with remote ambience server")
                    else:
                        system.status.active = True
                else:
                    pass
            else:
                if comm.sendUpdate() == False:
                    while comm.connect() == False:
                        pass
                    if comm.sendUpdate() == False:
                        raise Exception("Connect error. Unable to communicate with remote ambience server")
                    else:
                        system.status.active = True
                else:
                    pass
            
    def getEnigma():
        i = 0
        while i < globals.maxY:
            n = 0
            while n < 200:
                pytools.IO.console.printAt(n, i, "          ")
                n = n + 10
            i = i + 1
        print("Enigma Encoder")
        print("--------------")
        salt = tools.inputOption("Please enter the salt (integer): ", int)
        rotors = tools.inputOption("Please enter the number of rotors (integer): ", int)
        plugboard = tools.inputOption("Please enter the plugboard key (string): ", str)
        flags.enigmaSettings = {
            "salt": salt,
            "rotors": rotors,
            "plugboard": plugboard
        }
        pytools.cipher.enigma.enigma.init(salt, rotors, plugboard)
        
    def changeCred():
        if os.path.exists("server.json"):
            cred = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "server.json", False)
        else:
            cred = {
                "username": "",
                "password": ""
            }
        system.getEnigma()
        exitn = True
        while exitn:
            username = tools.inputOption("Please enter your username: ", str)
            usernameConf = tools.inputOption("Please enter your username: ", str)
            if username == usernameConf:
                cred["username"] = pytools.cipher.enigma.work.encode(username)
                exitn = False
            else:
                print("Please correct username issues.")
        
        exitn = True
        while exitn:
            username = tools.inputOption("Please enter your password: ", str)
            usernameConf = tools.inputOption("Please enter your password: ", str)
            if username == usernameConf:
                cred["password"] = pytools.cipher.enigma.work.encode(username)
                exitn = False
            else:
                print("Please password username issues.")
        pytools.IO.saveJson("\\\\" + flags.remote + "\\ambience\\" + "server.json", cred)
        print("changed.")
        
    def checkCred(bypass=False):
        i = 0
        while i < globals.maxY:
            n = 0
            while n < 200:
                pytools.IO.console.printAt(n, i, "          ")
                n = n + 10
            i = i + 1
        if bypass == False:
            if os.path.exists("server.json"):
                cred = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "server.json", False)
            else:
                system.changeCred()
                cred = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "server.json", False)
            if cred["username"] == "":
                if cred["password"] == "":
                    system.changeCred()
        if bypass == False:
            if flags.enigma == False:
                system.getEnigma()
            else:
                pytools.cipher.enigma.enigma.init(flags.enigmaSettings["salt"], flags.enigmaSettings["rotors"], flags.enigmaSettings["plugboard"])
        else:
            pytools.cipher.enigma.enigma.init(flags.enigmaSettings["salt"], flags.enigmaSettings["rotors"], flags.enigmaSettings["plugboard"])
        check = True
        if bypass:
            if cred["username"] == "":
                if cred["password"] == "":
                    check = False
        if check:
            username = tools.inputOption("Please enter your username: ", str)
            password = tools.inputOption("Please enter your password: ", str)
            if cred["username"] == pytools.cipher.enigma.work.encode(username):
                if cred["password"] == pytools.cipher.enigma.work.encode(password):
                    flags.enigma = True
                    return True
        else:
            return True
        return False
    
    def stop():
        if flags.remote == False:
            subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "taskkill /f /im ambience.exe")[0]
            subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "taskkill /f /im clock.exe")[0]
            subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "taskkill /f /im fireplace.exe")[0]
            subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "taskkill /f /im generic.exe")[0]
            subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "taskkill /f /im window.exe")[0]
            subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "taskkill /f /im outside.exe")[0]
            subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "taskkill /f /im windown.exe")[0]
            subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "taskkill /f /im light.exe")[0]
            pytools.IO.saveFile("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\clocks\\running\\gwcont.derp", "derp")
            pytools.IO.saveFile("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\clocks\\running\\wcont.derp", "derp")
            system.status.active = False
        else:
            while comm.connect() == False:
                pass
            if comm.sendStop() == False:
                while comm.connect() == False:
                    pass
                if comm.sendStop() == False:
                    raise Exception("Connect error. Unable to communicate with remote ambience server")
                else:
                    system.status.active = False
            else:
                system.status.active = False
    
    class status:
        active = False

class menu:
    def handler():
        try:
            menu.main()
            if (flags.monitor == False):
                system.stop()
            exit(0)
        except:
            flags.exitf = True
            if (flags.monitor == False):
                system.stop()
            raise Exception("Exiting...")
    
    def main():
        f = True
        j = False
        h = False
        while True:
            try:
                if (pytools.clock.getDateTime()[5] % 30) == 0:
                    try:
                        subprocess.getstatusoutput("net start w32time")
                        subprocess.getstatusoutput("w32tm /resync")
                    except:
                        pass
                if f:
                    error = subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "choice /c mt /n")[0]
                    
                if error == 1:
                    f = True
                    flags.display = False
                    time.sleep(0.5)
                    i = 0
                    while i < globals.maxY:
                        n = 0
                        while n < 200:
                            pytools.IO.console.printAt(n, i, "          ")
                            n = n + 10
                        i = i + 1
                    printColor(0, 0, "Main Menu", "green")
                    printColor(0, 1, "---------", "green")
                    printColor(0, 3, "(r) - Return", "green")
                    printColor(0, 4, "(p) - Open Plugin Inspector", "green")
                    upn = 0
                    if flags.monitor == False:
                        upn = 3
                        printColor(0, 5, "(s) - Start System", "green")
                        printColor(0, 6, "(h) - Stop System", "green")
                        printColor(0, 7, "(c) - Change Login Credentials", "green")
                    elif flags.bypass:
                        upn = 3
                        printColor(0, 5, "(s) - Start System", "green")
                        printColor(0, 6, "(h) - Stop System", "green")
                        printColor(0, 7, "(c) - Change Login Credentials", "green")
                    printColor(0, 5 + upn, "(e) - Exit", "green")
                    if j:
                        printColor(0, 9, "---Error: Please start system before opening plugin menu.", "red")
                        j = False
                    if h:
                        printColor(0, 9, "---Error: Username and/or password incorrect.", "red")
                        h = False
                    error = subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "choice /c rpshce /n")[0]
                    if error == 1:
                        i = 0
                        while i < globals.maxY:
                            n = 0
                            while n < 200:
                                pytools.IO.console.printAt(n, i, "          ")
                                n = n + 10
                            i = i + 1
                        flags.display = True
                    if error == 2:
                        if system.status.active == True:
                            menu.pluginMenu()
                        else:
                            j = True
                        f = False
                    if (flags.monitor == False) or flags.bypass:
                        if error == 3:
                            if system.checkCred():
                                system.start()
                            else:
                                h = True
                            f = False
                        if error == 4:
                            if system.checkCred():
                                system.stop()
                            else:
                                h = True
                            f = False
                        if error == 5:
                            if system.checkCred(True):
                                system.changeCred()
                            else:
                                h = True
                            f = False
                    else:
                        if 3 <= error <= 5:
                            f = False
                    if error == 6:
                        flags.exitf = True
                        return 0
                    
                if error == 2:
                    globals.forecastLength = (not globals.forecastLength)
            except:
                printColor(0, 0, traceback.format_exc(), "red")
                
    plugN = 0
    plugI = 0
    plugR = False
    strF = " -------------------------------------------------------------------"
    plugF = 0
    
    def pluginMenu():
        f = True
        while f:
            i = 0
            while i < globals.maxY:
                n = 0
                while n < 200:
                    pytools.IO.console.printAt(n, i, "          ")
                    n = n + 10
                i = i + 1
            keys = "0123456789abcdefghijklmnopqstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            letters = "r"
            i = 0
            choices = {}
            printColor(0, 0, "Plugin Inspector", "green")
            printColor(0, 1, "----------------", "green")
            printColor(0, 3, "(r) - Return to main menu.", "green")
            for plugin in os.listdir(".\\vars\\pluginVarsjson"):
                printColor(0, i + 4, "(" + keys[i] + ") - Plugin " + plugin.split("_keys")[0] + ".", "green")
                choices[i + 2] = plugin
                letters = letters + keys[i]
                i = i + 1
            choice = subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "choice /c " + letters + " /n /cs")[0]
            if choice != 1:
                plugin = choices[choice]
                menu.plugN = 2
                menu.plugI = 0
                printColor(40, 0, plugin, "green")
                json = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\" + plugin, False)
                for key in json:
                    menu.readInfo(json[key], key)
                    menu.plugN = menu.plugN + 1
                    if menu.plugN > (globals.maxY - 1):
                        menu.plugN = 0
                        menu.plugI = menu.plugI + 40
                printColor(40 + menu.plugI, menu.plugN + 1, "(r) - Return to plugin menu.", "green")
                if os.path.exists(".\\vars\\plugins\\plugin." + plugin.split("_keys")[0] + ".run()-error.cx"):
                    printColor(40 + menu.plugI, menu.plugN + 2, "(v) - View errors.", "green")
                error = subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "choice /c rv /n")[0]
                if os.path.exists(".\\vars\\plugins\\plugin." + plugin.split("_keys")[0] + ".run()-error.cx"):
                    if error == 2:
                        f = pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\" + plugin.split("_keys.json")[0] + "_errorlog.log", False).split("\n")
                        printColor(40 + menu.plugI, menu.plugN + 3, "", "green")
                        menu.plugN = menu.plugN + 1
                        menu.plugN = menu.plugN + 1
                        if len(f) > 10:
                            for m in f[-10:]:
                                printColor(40 + menu.plugI, menu.plugN + 3, m, "green")
                                menu.plugN = menu.plugN + 1
                        else:
                            for m in f:
                                printColor(40 + menu.plugI, menu.plugN + 3, m, "green")
                                menu.plugN = menu.plugN + 1
                        printColor(40 + menu.plugI, menu.plugN + 5, "(r) - Return to plugin menu.", "green")
                        error = subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "choice /c r /n")[0]
            else:
                f = False
        
    
    def readInfo(json, key):
        menu.plugF = menu.plugF + 1
        if str(json)[0] == "{":
            if menu.plugR:
                menu.plugN = menu.plugN + 1
                if menu.plugN > (globals.maxY - 1):
                    menu.plugN = 0
                    menu.plugI = menu.plugI + 40
                menu.plugR = False
            printColor(40 + menu.plugI, menu.plugN, menu.strF[0:menu.plugF] + str(key) + ":", "green")
            menu.plugN = menu.plugN + 1
            if menu.plugN > (globals.maxY - 1):
                menu.plugN = 0
                menu.plugI = menu.plugI + 40
            for keyf in json:
                menu.readInfo(json[keyf], keyf)
                menu.plugN = menu.plugN + 1
                if menu.plugN > (globals.maxY - 1):
                    menu.plugN = 0
                    menu.plugI = menu.plugI + 40
        elif str(json)[0] == "[":
            printColor(40 + menu.plugI, menu.plugN, menu.strF[0:menu.plugF] + str(key) + ":", "green")
            menu.plugN = menu.plugN + 1
            if menu.plugN > (globals.maxY - 1):
                menu.plugN = 0
                menu.plugI = menu.plugI + 40
            i = 0
            for keyf in json:
                menu.readInfo(keyf, "-" + str(i))
                i = i + 1
                menu.plugN = menu.plugN + 1
                if menu.plugN > (globals.maxY - 1):
                    menu.plugN = 0
                    menu.plugI = menu.plugI + 40
        else:
            printColor(40 + menu.plugI, menu.plugN, menu.strF[0:menu.plugF] + str(key) + ": " + str(json), "green")
            menu.plugR = True
        menu.plugF = menu.plugF - 1
            
        
def printColor(x, y, text, color):
    
    attrs = []
    if color == "grey":
        attrs = ['bold']
    if color == "black":
        color = "grey"
        attrs = ["dark"]
    if "light" in color:
        attrs = ['bold']
        color = color.replace("light_", "")
    if "dark" in color:
        attrs = ['dark']
        color = color.replace("dark_", "")
    
    subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "color")[0]
    pytools.IO.console.printAt(x, y, termcolor.colored(text, color, attrs=attrs))

spaces = "                                                                    "

def getSection():
    dateArray = pytools.clock.getDateTime()
    dayTimes = pytools.IO.getList(".\\working\\daytimes.pyl", False)[1]
    phases = ["Daylight Phase", "Uncanny Phase", "Dark Phase", "Evil Phase", "Sinister Phase", "Dying Phase P1", "Dying Phase P2", "Dying Phase P3", "Dying Phase P4", "Death Phase", "Necro Phase", "Reserect Phase", "Safe Phase"]
    if pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5]):
        if globals.hallowIndex > 0:
            if dateArray[3] < (dayTimes[2][3] - 1):
                return phases[10]
            elif dateArray[3] == (dayTimes[2][3] - 1):
                return phases[11]
            elif dateArray[3] == (dayTimes[2][3]):
                return phases[12]
            return phases[0]
        else:
            if dateArray[3] < (dayTimes[2][3] - 1):
                return phases[12]
            elif dateArray[3] == (dayTimes[2][3] - 1):
                return phases[12]
            elif dateArray[3] == (dayTimes[2][3]):
                return phases[12]
            return phases[0]
    else:
        if dateArray[3] > 12:
            if dateArray[3] < 22:
                if globals.hallowIndex > 0:
                    try:
                        if pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["death_wind"]["state"] == 0:
                            return phases[1]
                        else:
                            try:
                                if pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["monsters"]["state"] == 0:
                                    return phases[2]
                                else:
                                    try:
                                        if pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["ghosts"]["state"] == 0:
                                            return phases[3]
                                        else:
                                            return phases[4]
                                    except:
                                        return phases[3]
                            except:
                                return phases[2]
                    except:
                        return phases[1]
                
                if globals.hallowIndex > -5:
                    try:
                        if pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["death_wind"]["state"] == 0:
                            return phases[1]
                        else:
                            try:
                                if pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["monsters"]["state"] == 0:
                                    return phases[1]
                                else:
                                    try:
                                        if pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["ghosts"]["state"] == 0:
                                            return phases[1]
                                        else:
                                            return phases[1]
                                    except:
                                        return phases[1]
                            except:
                                return phases[1]
                    except:
                        return phases[1]
                
                else:
                    return phases[12]
            
            elif dateArray[3] == 22:
                if globals.hallowIndex > 0:
                    if dateArray[4] < 15:
                        return phases[5]
                    if dateArray[4] < 30:
                        return phases[6]
                    if dateArray[4] < 45:
                        return phases[7]
                    if dateArray[4] >= 45:
                        return phases[8]
                elif globals.hallowIndex > -5:
                    if dateArray[4] < 15:
                        return phases[1]
                    if dateArray[4] < 30:
                        return phases[1]
                    if dateArray[4] < 45:
                        return phases[1]
                    if dateArray[4] >= 45:
                        return phases[1]
                else:
                    return phases[0]
            elif dateArray[3] == 23:
                if globals.hallowIndex > 0:
                    return phases[9]
                if globals.hallowIndex > -5:
                    return phases[2]
                if globals.hallowIndex > -7:
                    return phases[1]
                else:
                    return phases[0]
                    

class displayObject:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.data = [" " * width] * height
    
    def set(self, x, y, char):
        if len(char):
            char = char[0]
            self.data[y] = self.data[y][:x] + char + self.data[y][x + 1:]
            
    def get(self, x, y):
        return self.data[y][x]
        
def main():
    try:
        
        horrorForecastDisplay = displayObject(10, 60)
        extendedHorrorForecastDisplay = displayObject(10, 60)
        
        i = 0
        flash = 0
        restartMod = 0
        while i < globals.maxY:
            n = 0
            while n < 200:
                pytools.IO.console.printAt(n, i, "          ")
                n = n + 10
            i = i + 1
        while True:
            if flags.defaultSystemState == True:
                if system.status.active != True:
                    if (pytools.clock.getDateTime()[5] % 5) == 0:
                        restartMod = restartMod + 1
                    if restartMod > 12:
                        system.stop()
                        system.start()
                        restartMod = 0
                else:
                    restartMod = 0
            try:
                if (pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\systemLoop.json", False) == "                                     "):
                    system.status.active = False
                else:
                    try:
                        if (pytools.clock.dateArrayToUTC(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\systemLoop.json", False)["loopTime"]) + 20) < (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())):
                            system.status.active = False
                        else:
                            system.status.active = True
                    except:
                        system.status.active = False
            except:
                system.status.active = False
            if flags.exitf == True:
                exit()
            if flags.display:
                if (pytools.clock.getDateTime()[5] % 30) == 0:
                    i = 0
                    while i < globals.maxY:
                        n = 0
                        while n < 200:
                            if flags.displayOnScreen:
                                pytools.IO.console.printAt(n, i, "          ")
                            n = n + 10
                        i = i + 1
                weather = pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\dispstring.cx", False)
                try:
                    gh = weather[0:23]
                except:
                    gh = ""
                if gh == 'Temperature (C)      : ':
                    
                    try:
                        lightningDanger = pytools.IO.getJson("\\\\" + tools.getRemote() + "\\ambience\\working\\lightningData.json")["dangerLevel"]
                    except:
                        lightningDanger = 0
                    
                    weather = weather.replace("\nCondition", "\nLightning   (danger) : " + str(lightningDanger) + "\nCondition")

                    system.status.active = True 
                    
                    if flags.displayOnScreen:
                        pytools.IO.console.printAt(0, 0, "Ambience System Console")
                        pytools.IO.console.printAt(0, 1, "-----------------------")
                        # pytools.IO.console.printAt(0, 3, weather)
                        
                        __g = {
                            0: "temperature",
                            1: "wind",
                            2: "wind",
                            3: "pressure",
                            4: "rain",
                            5: "humidity",
                            6: "lightning",
                            7: "condition"
                        }
                        
                        try:
                            _n = 3
                            _g = 0
                            for _cond in weather.split("\n"):
                                if _g in __g:
                                    printColor(0, _n, _cond.split(":")[0] + ":", "white")
                                    printColor(len(_cond.split(":")[0] + ":"), _n, _cond.split(":")[1], tools.getWeatherColor(_cond.split(":")[1], __g[_g]))
                                else:
                                    pytools.IO.console.printAt(0, _n, _cond)
                                    
                                _n = _n + 1
                                _g = _g + 1
                        except:
                            print(_cond.split(":")[1])
                            print(traceback.format_exc())
                        
                    if flags.webMode:
                        pytools.IO.saveFile(flags.webMode + "\\conditions.txt", weather)
                    i = 4 + len(weather.split("\n"))
                    if os.path.exists("\\\\" + tools.getRemote() + "\\ambience\\vars\\pluginVarsJson") == False:
                        subprocess.getstatusoutput("pushd \"\\" + tools.getRemote() + "\\ambience\" & " + "mkdir \"" + "\\\\" + tools.getRemote() + "\\ambience\\vars\\pluginVarsJson" + "\"")[0]
                    if flags.displayOnScreen:
                        getList = {}
                        getErrorList = {}
                        for plugin in os.listdir("\\\\" + tools.getRemote() + "\\ambience\\vars\\pluginVarsJson"):
                            getList[plugin] = ".\\vars\\pluginVarsJson\\" + plugin
                            getErrorList[plugin] = ".\\vars\\plugins\\plugin." + plugin.split("_keys")[0] + ".run()-error.cx"
                        outList = getMultiJson(getList)
                        outErrorList = getMultiFile(getErrorList)
                        for plugin in getList:
                            
                            if plugin[-6:] != "_error":
                                if flags.displayOnScreen:
                                    try:
                                        pytools.IO.console.printAt(2, i, plugin.split("_keys")[0][0:19])
                                    except:
                                        pass
                                try:
                                    pInfo = outList[".\\vars\\pluginVarsJson\\" + plugin]
                                except:
                                    pass
                                if system.status.active == True:
                                    if flags.displayOnScreen:
                                        if os.path.exists(".\\vars\\plugins\\plugin." + plugin.split("_keys")[0] + ".run()-error.cx"):
                                            if flash == 0:
                                                try:
                                                    if (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC(pInfo["lastLoop"])) > 600:
                                                        printColor(0, i, "!", "red")
                                                    else:
                                                        printColor(0, i, "!", "yellow")
                                                except:
                                                    printColor(0, i, "!", "red")
                                            else:
                                                pytools.IO.console.printAt(0, i, " ")
                                        else:
                                            pytools.IO.console.printAt(0, i, " ")
                                if flags.displayOnScreen:
                                    if system.status.active == True:
                                        try:
                                            pytools.IO.console.printAt(20, i, " : ")
                                            if (pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - pytools.clock.dateArrayToUTC(pInfo["lastLoop"])) > 600:
                                                printColor(23, i, "Inactive." + spaces[len("Inactive."):14], "yellow")
                                            else:
                                                printColor(23, i, "Active." + spaces[len("Active."):14], "green")
                                        except:
                                            printColor(23, i, "Nonresponsive.", "red")
                                    else:
                                        printColor(23, i, "Offline." + spaces[len("Offline."):14], "magenta")
                                i = i + 1
                    
                    y = i
                    
                    try:
                        
                        def _soundSortKey(x):
                            return x.split(';')[-1]
                        
                        soundsClock = sorted(pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\sounds\\clock.cxl", False).split("\n"), key=_soundSortKey)
                        soundsFireplace = sorted(pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\sounds\\fireplace.cxl", False).split("\n"), key=_soundSortKey)
                        soundsOutside = sorted(pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\sounds\\outside.cxl", False).split("\n"), key=_soundSortKey)
                        soundsWindow = sorted(pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\sounds\\window.cxl", False).split("\n"), key=_soundSortKey)
                        
                        soundsClock.remove("")
                        soundsFireplace.remove("")
                        soundsOutside.remove("")
                        soundsWindow.remove("")
                        
                        
                    except:
                        pass
                    
                    def isWait(f, baseColor="white"):
                        if f.split(";")[-1][0:2] == "h ":
                            return "yellow"
                        if f.split(";")[-1][0:2] == "g ":
                            return "cyan"
                        if "midnight" in f.split(";")[-1]:
                            return "red"
                        if ("dark" in f.split(";")[-1]) and ("junco" not in f.split(";")[-1]):
                            return "red"
                        if "sinister" in f.split(";")[-1]:
                            return "yellow"
                        if "death wind" in f.split(";")[-1]:
                            return "cyan"
                        if "monster" in f.split(";")[-1]:
                            return "yellow"
                        if "knock" in f.split(";")[-1]:
                            return "yellow"
                        if "ghosts" in f.split(";")[-1]:
                            return "red"
                        if "death" in f.split(";")[-1]:
                            return "red"
                        if f.split(";")[2] != "0":
                            if baseColor == "grey":
                                return "white"
                            return "grey"
                        if "christmas" in f.split(";")[-1]:
                            return "light_green"
                        if "thunder" in f.split(";")[-1]:
                            return "light_blue"
                        if "blowing" in f.split(";")[-1]:
                            return "light_cyan"
                        if "bell" in f.split(";")[-1]:
                            return "light_yellow"
                        
                        try:
                            if (f.split(";")[-1][0] == "s") and str(int(f.split(";")[-1][1])):
                                return "light_red"
                        except:
                            pass
                        
                        return baseColor
                    
                    try:
                        
                        clockSpeakerColor = "white"
                        if (pytools.clock.getDateTime()[4] % 15) == 0:
                            clockSpeakerColor = "light_green"
                        
                        if flags.displayOnScreen:
                            printColor(60, 0, "Clock Speaker Sounds", color=clockSpeakerColor)
                            printColor(60, 1, "--------------------", color=clockSpeakerColor)
                        fileOutput = ""
                        i = 3
                        for f in soundsClock:
                            if system.status.active == True:
                                if flags.displayOnScreen:
                                    
                                    if "]" in f.split(";")[0]:
                                        f = ";".join([f.split(";")[0].split(",")[0], *(f.split(";")[1:])])
                                    
                                    printColor(50, i, (str(round(float(f.split(";")[1]), 2)) + "0")[:4] + spaces[len((str(round(float(f.split(";")[1]), 2)) + "0")[:4]):5], color=tools.getValueColor(float(f.split(";")[1]), "speed"))
                                    printColor(55, i, str(round(float(f.split(";")[0]), 2))[:4] + spaces[len(str(round(float(f.split(";")[0]), 2))[:4]):5], color=tools.getValueColor(float(f.split(";")[0])))
                                    printColor(60, i, (f.split(";")[-1])[:20] + spaces[len((f.split(";")[-1])[:20]):20], color=isWait(f, baseColor=clockSpeakerColor))
                                fileOutput = fileOutput + "\n" + f + spaces[len(f):30]
                                i = i + 1
                        if flags.webMode:
                            pytools.IO.saveFile(flags.webMode + "\\clockSounds.txt", fileOutput)
                        if flags.displayOnScreen:
                            f = i
                            while i < (f + 10):
                                pytools.IO.console.printAt(50, i, spaces[0:30])
                                i = i + 1
                    except:
                        pass
                    
                    try:
                        try:
                            if pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\fireplace.json")["fireplaceStage"] in ["fireEnd", "fireStart"]:
                                fireplaceSpeakerColor = "yellow"
                            elif pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\fireplace.json")["fireplaceStage"] in ["match"]:
                                fireplaceSpeakerColor = "light_red"
                            elif pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\fireplace.json")["fireplaceStage"] not in ["firePrep", "out", "fireLoad"]:
                                fireplaceSpeakerColor = "light_yellow"
                            elif pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\data.json")["data"][0][1] < 10:
                                fireplaceSpeakerColor = "grey"
                            else:
                                fireplaceSpeakerColor = "white"
                        except:
                            fireplaceSpeakerColor = "red"
                        
                        if flags.displayOnScreen:
                            printColor(95, 0, "Fireplace Speaker Sounds", color=fireplaceSpeakerColor)
                            printColor(95, 1, "------------------------", color=fireplaceSpeakerColor)
                        fileOutput = ""
                        i = 3
                        for f in soundsFireplace:
                            if system.status.active == True:
                                if flags.displayOnScreen:
                                    
                                    if "]" in f.split(";")[0]:
                                        f = ";".join([f.split(";")[0].split(",")[0], *(f.split(";")[1:])])
                                    
                                    printColor(85, i, (str(round(float(f.split(";")[1]), 2)) + "0")[:4] + spaces[len((str(round(float(f.split(";")[1]), 2)) + "0")[:4]):5], color=tools.getValueColor(float(f.split(";")[1]), "speed"))
                                    printColor(90, i, str(round(float(f.split(";")[0]), 2))[:4] + spaces[len(str(round(float(f.split(";")[0]), 2))[:4]):5], color=tools.getValueColor(float(f.split(";")[0])))
                                    printColor(95, i, (f.split(";")[-1])[:20] + spaces[len((f.split(";")[-1])[:20]):20], color=isWait(f, baseColor=fireplaceSpeakerColor))
                                fileOutput = fileOutput + "\n" + f + spaces[len(f):30]
                                i = i + 1
                        if flags.webMode:
                            pytools.IO.saveFile(flags.webMode + "\\fireplaceSounds.txt", fileOutput)
                        if flags.displayOnScreen:
                            f = i
                            while i < (f + 10):
                                pytools.IO.console.printAt(85, i, spaces[0:30])
                                i = i + 1
                    except:
                        pass
                    
                    try:
                        
                        if pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\nomufflewn.derp", False) != "1.0":
                            windowSpeakerColor = "white"
                        else:
                            windowSpeakerColor = "grey"
                            
                            
                        
                        if flags.displayOnScreen:
                            printColor(130, 0, "Window Speaker Sounds", color=windowSpeakerColor)
                            printColor(130, 1, "--------------------", color=windowSpeakerColor)
                        fileOutput = ""
                        i = 3
                        for f in soundsWindow:
                            if system.status.active == True:
                                if flags.displayOnScreen:
                                    
                                    if "]" in f.split(";")[0]:
                                        f = ";".join([f.split(";")[0].split(",")[0], *(f.split(";")[1:])])
                                    
                                    printColor(120, i, (str(round(float(f.split(";")[1]), 2)) + "0")[:4] + spaces[len((str(round(float(f.split(";")[1]), 2)) + "0")[:4]):5], color=tools.getValueColor(float(f.split(";")[1]), "speed"))
                                    printColor(125, i, str(round(float(f.split(";")[0]), 2))[:4] + spaces[len(str(round(float(f.split(";")[0]), 2))[:4]):5], color=tools.getValueColor(float(f.split(";")[0])))
                                    printColor(130, i, (f.split(";")[-1])[:20] + spaces[len((f.split(";")[-1])[:20]):20], color=isWait(f, baseColor=windowSpeakerColor))
                                fileOutput = fileOutput + "\n" + f + spaces[len(f):30]
                                i = i + 1
                        if flags.webMode:
                            pytools.IO.saveFile(flags.webMode + "\\windowSounds.txt", fileOutput)
                        if flags.displayOnScreen:
                            f = i
                            while i < (f + 10):
                                pytools.IO.console.printAt(120, i, spaces[0:30])
                                i = i + 1
                    except:
                        pass
                    
                    try:
                        outsideSpeakerColor = tools.colorMult(tools.getWeatherColor(str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\data.json")["data"][0][7]), typef="temperature"), tools.colorMult(tools.getWeatherColor(str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\data.json")["data"][0][4]), typef="condition"), tools.getWeatherColor(str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\data.json")["data"][0][6]), typef="pressure")))
                        
                        if (pytools.clock.getDateTime()[3] < 5) or (pytools.clock.getDateTime()[3] > 20):
                            outsideSpeakerColor = tools.colorMult(outsideSpeakerColor, "black")
                        
                        if outsideSpeakerColor == "black":
                            outsideSpeakerColor = "grey"
                    except:
                        outsideSpeakerColor = "white"
                        
                        if (pytools.clock.getDateTime()[3] < 5) or (pytools.clock.getDateTime()[3] > 20):
                            outsideSpeakerColor = "grey"
                    
                    try:
                        if flags.displayOnScreen:
                            printColor(165, 0, "Outside Speaker Sounds", color=outsideSpeakerColor)
                            printColor(165, 1, "--------------------", color=outsideSpeakerColor)
                        fileOutput = ""
                        i = 3
                        for f in soundsOutside:
                            if system.status.active == True:
                                if flags.displayOnScreen:
                                    
                                    if "]" in f.split(";")[0]:
                                        f = ";".join([f.split(";")[0].split(",")[0], *(f.split(";")[1:])])
                                    
                                    printColor(155, i, (str(round(float(f.split(";")[1]), 2)) + "0")[:4] + spaces[len((str(round(float(f.split(";")[1]), 2)) + "0")[:4]):5], color=tools.getValueColor(float(f.split(";")[1]), "speed"))
                                    printColor(160, i, str(round(float(f.split(";")[0]), 2))[:4] + spaces[len(str(round(float(f.split(";")[0]), 2))[:4]):5], color=tools.getValueColor(float(f.split(";")[0])))
                                    printColor(165, i, (f.split(";")[-1])[:20] + spaces[len((f.split(";")[-1])[:20]):20], color=isWait(f, baseColor=outsideSpeakerColor))
                                fileOutput = fileOutput + "\n" + f + spaces[len(f):30]
                                i = i + 1
                        if flags.webMode:
                            pytools.IO.saveFile(flags.webMode + "\\outsideSounds.txt", fileOutput)
                        if flags.displayOnScreen:
                            f = i
                            while i < (f + 10):
                                pytools.IO.console.printAt(155, i, spaces[0:30])
                                i = i + 1
                    except:
                        pass
                    
                    try:
                        if flags.displayOnScreen:
                            clients = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\hosts.json", doPrint=False)
                            clientsData = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\hostData.json", doPrint=False)
                        
                        if flags.displayOnScreen:
                            pytools.IO.console.printAt(130, globals.maxY - 1, "Ambience Client Information                     ")
                            pytools.IO.console.printAt(130, globals.maxY - 2, "------------------------------------------------")
                            pytools.IO.console.printAt(130, globals.maxY - 3, " IP            STATUS     MAX CUR SSTC MCPU OPEN")
                            pytools.IO.console.printAt(130, globals.maxY - 4, "                                                ")
                        
                        totalSounds = 0
                        maxSounds = 0
                        i = 2
                        if flags.displayOnScreen:
                            if "127.0.0.1" not in clients["hosts"]:
                                clients["hosts"].append("127.0.0.1")
                                
                            if "127.0.0.1" not in clientsData:
                                
                                if globals.lastServerGrab < time.time():
                                    clientsData["127.0.0.1"] = {}
                                    try:
                                        clientsData["127.0.0.1"]["max"] = pytools.net.getJsonAPI("http://" + str(flags.remote) + ":5597?json=" + urllib.parse.quote(json.dumps({
                                            "command": "getMaxSoundCount"
                                        })), timeout=1)["maxSoundCount"]
                                    except:
                                        clientsData["127.0.0.1"]["max"] = 0
                                        
                                    try:
                                        clientsData["127.0.0.1"]["current"] = pytools.net.getJsonAPI("http://" + str(flags.remote) + ":5597?json=" + urllib.parse.quote(json.dumps({
                                            "command": "getSoundCount"
                                        })), timeout=1)["soundCount"]
                                    except:
                                        clientsData["127.0.0.1"]["current"] = 0
                                        
                                    if clientsData["127.0.0.1"]["current"] >= clientsData["127.0.0.1"]["max"]:
                                        clientsData["127.0.0.1"]["play"] = False
                                    else:
                                        clientsData["127.0.0.1"]["play"] = True
                                    
                                    try:
                                        clientsData["127.0.0.1"]["MCPU"] = pytools.net.getJsonAPI("http://" + str(flags.remote) + ":5597?json=" + urllib.parse.quote(json.dumps({"command":"getCpuUsage"})), timeout=1)["cpuUsage"]
                                    except:
                                        if "MCPU" not in clientsData["127.0.0.1"]:
                                            clientsData["127.0.0.1"]["MCPU"] = 0
                                            
                                    globals.serverData = clientsData["127.0.0.1"]
                                    globals.lastServerGrab = time.time() + 5
                                else:
                                    clientsData["127.0.0.1"] = globals.serverData
                                    
                            for client in clients["hosts"]:
                                if client != "0.0.0.0":
                                    try:

                                        try:
                                            if not client in globals.lastSSTCGrabs:
                                                globals.lastSSTCGrabs[client] = [0, 0, 0]
                                            if globals.lastSSTCGrabs[client][0] < time.time():
                                                if ((int(math.floor(time.time() / 5)) * 5) % 10) == 0:
                                                    if str(client) != "127.0.0.1":
                                                        SSTCData = pytools.net.getJsonAPI("http://" + str(client) + ":4507?json=" + urllib.parse.quote(json.dumps({"command":"getSleepStateCount"})), timeout=1)["sleepStateCount"]
                                                    else:
                                                        SSTCData = globals.lastSSTCGrabs[client][1]
                                                    MCPUData = globals.lastSSTCGrabs[client][2]
                                                else:
                                                    SSTCData = globals.lastSSTCGrabs[client][1]
                                                    try:
                                                        if str(client) != "127.0.0.1":
                                                            MCPUData = pytools.net.getJsonAPI("http://" + str(client) + ":4507?json=" + urllib.parse.quote(json.dumps({"command":"getCPUUsageThreshold"})), timeout=1)["cpuUsageThreshold"]
                                                        else:
                                                            MCPUData = pytools.net.getJsonAPI("http://" + str(flags.remote) + ":5597?json=" + urllib.parse.quote(json.dumps({"command":"getCpuUsage"})), timeout=1)["cpuUsage"]
                                                    except:
                                                        try:
                                                            MCPUData = globals.lastSSTCGrabs[client][2]
                                                        except:
                                                            MCPUData = -1
                                                globals.lastSSTCGrabs[client][0] = time.time() + 5
                                                globals.lastSSTCGrabs[client][1] = SSTCData
                                                globals.lastSSTCGrabs[client][2] = MCPUData
                                            else:
                                                SSTCData = globals.lastSSTCGrabs[client][1]
                                                MCPUData = globals.lastSSTCGrabs[client][2]
                                            
                                        except:
                                            SSTCData = 0
                                        
                                        _clientSpaceAdder = 12 - len(client)
                                        if _clientSpaceAdder < 0:
                                            _clientSpaceAdder = 0
                                            
                                        if client == "127.0.0.1":
                                            pytools.IO.console.printAt(131, globals.maxY - 3 - i, client + "             " + (" " * _clientSpaceAdder) + str(int(clientsData[client]["max"]) + 1) + spaces[len(str(int(clientsData[client]["max"]))):3] + " " + str(int(clientsData[client]["current"])) + spaces[len(str(int(clientsData[client]["current"]))):3] + " " + str(SSTCData) + (" " * (4 - len(str(SSTCData)))) + " " + (str(round(clientsData["127.0.0.1"]["MCPU"], 1))) + (" " * (5 - len(str(round(clientsData["127.0.0.1"]["MCPU"], 1))))) + str(clientsData[client]["play"]) + spaces[len(str(clientsData[client]["play"])):5])
                                        else:
                                            try:
                                                pytools.IO.console.printAt(131, globals.maxY - 3 - i, client + "             " + (" " * _clientSpaceAdder) + str(int(clientsData[client]["max"]) + 1) + spaces[len(str(int(clientsData[client]["max"]))):3] + " " + str(int(clientsData[client]["current"])) + spaces[len(str(int(clientsData[client]["current"]))):3] + " " + str(SSTCData) + (" " * (4 - len(str(SSTCData)))) + " " + (str(round(MCPUData, 1))) + (" " * (5 - len(str(round(MCPUData, 1))))) + str(clientsData[client]["play"]) + spaces[len(str(clientsData[client]["play"])):5])
                                            except:
                                                pytools.IO.console.printAt(131, globals.maxY - 3 - i, client + "  no data.      ")
                                        if clientsData[client]["current"] > clientsData[client]["max"] + 1:
                                            if flags.displayOnScreen:
                                                
                                                try:
                                                    lastErrorTimestamp = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\lastBufferErrorTime_" + str(client) + ".json", doPrint=False)["timeStamp"]
                                                except:
                                                    lastErrorTimestamp = [1, 1, 1, 0, 0, 0]
                                            
                                                if (pytools.clock.dateArrayToUTC(lastErrorTimestamp) + 15) > pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                                                    if flash == 0:
                                                        printColor(130, globals.maxY - 3 - i, "!", "yellow")
                                                    else:
                                                        printColor(130, globals.maxY - 3 - i, " ", "yellow")
                                                    printColor(145, globals.maxY - 3 - i, "problem", "cyan")
                                                else:
                                                    
                                                    printColor(145, globals.maxY - 3 - i, "overload", "red")
                                                    if flash == 0:
                                                        printColor(130, globals.maxY - 3 - i, "!", "yellow")
                                                    else:
                                                        printColor(130, globals.maxY - 3 - i, " ", "yellow")
                                        else:
                                            if flags.displayOnScreen:
                                                try:
                                                    try:
                                                        lastErrorTimestamp = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\lastBufferErrorTime_" + str(client) + ".json", doPrint=False)["timeStamp"]
                                                    except:
                                                        lastErrorTimestamp = [1, 1, 1, 0, 0, 0]
                                                    if (pytools.clock.dateArrayToUTC(lastErrorTimestamp) + 8) > pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                                                        if flash == 0:
                                                            printColor(130, globals.maxY - 3 - i, "!", "yellow")
                                                        else:
                                                            printColor(130, globals.maxY - 3 - i, " ", "yellow")
                                                        printColor(145, globals.maxY - 3 - i, "underrun", "magenta")
                                                    elif pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\working\\" + ".\\host-" + str(client) + ".bl", doPrint=False) != 1:
                                                        if pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\working\\" + ".\\host-" + str(client) + ".se", doPrint=False) != 1:
                                                            if flash == 0:
                                                                printColor(130, globals.maxY - 3 - i, "<", "blue")
                                                            else:
                                                                printColor(130, globals.maxY - 3 - i, " ", "blue")
                                                        else:
                                                            if flash == 0:
                                                                printColor(130, globals.maxY - 3 - i, "!", "magenta")
                                                            else:
                                                                printColor(130, globals.maxY - 3 - i, " ", "magenta")
                                                        printColor(145, globals.maxY - 3 - i, "dozingoff", "blue")
                                                    else:
                                                        if pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\working\\" + ".\\host-" + str(client) + ".se", doPrint=False) != 1:
                                                            if flash == 0:
                                                                printColor(130, globals.maxY - 3 - i, "<", "yellow")
                                                            else:
                                                                printColor(130, globals.maxY - 3 - i, " ", "yellow")
                                                        else:
                                                            printColor(130, globals.maxY - 3 - i, " ", "yellow")
                                                        printColor(145, globals.maxY - 3 - i, "connected", "green")
                                                except:
                                                    printColor(130, globals.maxY - 3 - i, "!", "yellow")
                                                    printColor(145, globals.maxY - 3 - i, "unknown", "white")
                                    except:
                                        pytools.IO.saveFile("console-error.txt", traceback.format_exc())
                                        if flags.displayOnScreen:
                                            pytools.IO.console.printAt(131, globals.maxY - 3 - i, client + "  no data.      ")
                                            if flash == 0:
                                                printColor(130, globals.maxY - 3 - i, "!", "red")
                                            else:
                                                printColor(130, globals.maxY - 3 - i, " ", "red")
                                
                                try:
                                    totalSounds = totalSounds + clientsData[client]["current"]
                                except:
                                    pass
                                
                                try:
                                    if (pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\working\\" + ".\\host-" + str(client) + ".bl", doPrint=False) == 1) and (pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\working\\" + ".\\host-" + str(client) + ".se", doPrint=False) == 1):
                                        maxSounds = maxSounds + clientsData[client]["max"]
                                except:
                                    pass
                                i = i + 1
                        
                        if flags.displayOnScreen:
                            try:
                                outsideVolume = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "outsideProperties.json")["volume"]
                                outsideLimiter = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "outsideProperties.json")["limiter"]
                                gilTic = round(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "gil.json")["prevTic"], 5)
                                gilInterval = round(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "gil.json")["switchInterval"], 5)
                                threadCount = round(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "gil.json")["threadCount"], 5)
                                
                                
                                if flags.displayOnScreen:
                                    pytools.IO.console.printAt(131, globals.maxY - 3 - i - 1, "Outside Volume/Limiter (V / L) : " + str(round(outsideVolume, 3)) + "Db / " + str(round(outsideLimiter, 3)) + "Db")
                                    pytools.IO.console.printAt(131, globals.maxY - 3 - i - 2, "GIL (prevTic / switchInterval) : " + str(round(gilTic, 4)) + " / " + str(gilInterval))
                            except:
                                pass
                            
                            try:
                                storageSpace = pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\storageSpace.cx", doPrint=False)
                            except:
                                storageSpace = 0
                            
                            def _threadCountColor(x):
                                if x < 60:
                                    return "blue"
                                if x < 90:
                                    return "light_blue"
                                if x < 120:
                                    return "cyan"
                                if x < 150:
                                    return "light_cyan"
                                if x < 200:
                                    return "green"
                                if x < 280:
                                    return "light_green"
                                if x < 330:
                                    return "light_yellow"
                                if x < 380:
                                    return "yellow"
                                if x < 430:
                                    return "light_red"
                                return "red"
                            
                            pytools.IO.console.printAt(131, globals.maxY - 3 - i - 3, "Total Sounds                   : " + str(totalSounds) + " (" + str(int((totalSounds / maxSounds) * 100)) + "% of total)")
                            pytools.IO.console.printAt(131, globals.maxY - 3 - i - 4, "Storage Space Left             : " + str(storageSpace))
                            pytools.IO.console.printAt(131, globals.maxY - 3 - i - 5, "Current Thread Count           : ")
                            printColor(131 + len("Current Thread Count           : "), globals.maxY - 3 - i - 5, str(threadCount), color=_threadCountColor(threadCount))
                            pytools.IO.console.printAt(130, globals.maxY - 3 - i, "                                      ")
                            
                            
                            i = i + 3
                            fn = i
                            while i < (fn + 10):
                                if flags.displayOnScreen:
                                    pytools.IO.console.printAt(130, globals.maxY - 3 - i - 3, spaces[0:40])
                                i = i + 1

                    except:
                        pass
                    
                    try:
                        horrorForecast = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\hallowForecastHourly.json", False)[:60]
                        extendedHorrorForecast = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\hallowForecastBiHourly.json", False)[:60 + (60 * globals.forecastLength)]
                        
                        try:
                            globals.hallowIndex = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\hallowIndex.json", False)["noDay"]
                        except:
                            pass
                        
                        try:
                            if system.status.active == True:
                                if (max(extendedHorrorForecast) > 0) or os.path.exists(".\\working\\halloweenmode.derp") or os.path.exists(".\\working\\deathmode.derp") or os.path.exists(".\\working\\runningUncanny.derp") or os.path.exists(".\\working\\deathForecasted.derp"):
                                    if os.path.exists(".\\working\\halloweenmode.derp") or os.path.exists(".\\working\\deathmode.derp") or os.path.exists(".\\working\\runningUncanny.derp"):
                                        if flash == 0:
                                            if flags.displayOnScreen:
                                                printColor(30, globals.maxY - 11, "        X", "red")
                                                printColor(30, globals.maxY - 10, "       X X", "red")
                                                printColor(30, globals.maxY - 9, "      X   X", "red")
                                                printColor(30, globals.maxY - 8, "     X  X  X", "red")
                                                printColor(30, globals.maxY - 7, "    X   X   X", "red")
                                                printColor(30, globals.maxY - 6, "   X    X    X", "red")
                                                printColor(30, globals.maxY - 5, "  X           X", "red")
                                                printColor(30, globals.maxY - 4, " X      X      X", "red")
                                                printColor(30, globals.maxY - 3, "X               X", "red")
                                                printColor(30, globals.maxY - 2, "XXXXXXXXXXXXXXXXX", "red")
                                        else:
                                            r = 0
                                            while r < 14:
                                                pytools.IO.console.printAt(30, globals.maxY - r, "                  ")
                                                r = r + 1
                                    section = getSection()
                                    
                                    if globals.hallowIndex > 0:
                                        hallowColor = "red"
                                    elif globals.hallowIndex > -6:
                                        hallowColor = "yellow"
                                    else:
                                        if section == "Uncanny Phase":
                                            hallowColor = "yellow"
                                        else:
                                            hallowColor = "green"
                                    
                                    if flags.displayOnScreen:
                                        printColor(50, globals.maxY - 9, "DEATH NIGHT ACTIVITY " + str(globals.hallowIndex), hallowColor)
                                        printColor(50, globals.maxY - 8, "--------------------", hallowColor)
                                        printColor(50, globals.maxY - 6, "Hallow Index        : " + str(globals.hallowIndex) + "Hi" + spaces[0:10], hallowColor)
                                        if globals.hallowIndex > 0:
                                            try:
                                                printColor(50, globals.maxY - 5, "Horror Index        : " + pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\horrorIndex.cx", False) + "Hi" + spaces[0:10], hallowColor)
                                            except:
                                                printColor(50, globals.maxY - 5, "Horror Index        : " + "0" + "Hi" + spaces[0:10], "red")
                                            try:
                                                printColor(50, globals.maxY - 4, "Whispering Index    : " + str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["whisperIndex"]) + "Hi" + spaces[0:10], "red")
                                            except:
                                                printColor(50, globals.maxY - 4, "Whispering Index    : " + "0" + "Hi" + spaces[0:10], "red")
                                            try:
                                                printColor(50, globals.maxY - 3, "Hallowed Wolf Index : " + str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["hallowedWolfIndex"]) + "Hi" + spaces[0:10], "red")
                                            except:
                                                printColor(50, globals.maxY - 3, "Hallowed Wolf Index : " + "0" + "Hi" + spaces[0:10], "red")
                                        printColor(50, globals.maxY - 2, "Current Section     : " + section + spaces[0:10], hallowColor)
                                    
                                        # globals.hallowIndex = max(extendedHorrorForecast[0:3])
                                        # if max(horrorForecast[0:3]) > globals.hallowIndex:
                                        #     globals.hallowIndex = max(horrorForecast[0:3])
                                        
                                        maxValue = max(horrorForecast)
                                        minValue = sorted(horrorForecast)[2]
                                        
                                        stepValue = (maxValue - minValue) / 10
                                        
                                        ig = 0
                                        for x in horrorForecast:
                                            
                                            try:
                                                aY = int(9 - (math.floor(((x - minValue) / stepValue))))
                                            except:
                                                aY = 0
                                            anX = ig
                                            
                                            
                                            if aY < 0:
                                                aY = 0
                                                
                                            if aY > 9:
                                                aY = 9
                                            
                                            horrorForecastDisplay.set(anX, aY, "X")
                                            nY = 0
                                            while nY < 10:
                                                
                                                if nY != aY:
                                                    horrorForecastDisplay.set(anX, nY, " ")
                                                    
                                                nY = nY + 1
                                            
                                            ig = ig + 1
                                        
                                        maxValue = max(extendedHorrorForecast)
                                        extendedMinValue = sorted(extendedHorrorForecast)[2]
                                        
                                        extendedStepValue = (maxValue - extendedMinValue) / 10
                                        
                                        ig = 0
                                        for x in extendedHorrorForecast[:-1]:
                                            
                                            try:
                                                aY = int(0 + (math.floor(((maxValue - x) / extendedStepValue))))
                                            except:
                                                aY = 0
                                            anX = ig
                                            
                                            if aY < 0:
                                                aY = 0
                                                
                                            if aY > 9:
                                                aY = 9
                                            
                                            extendedHorrorForecastDisplay.set(anX, aY, "X")
                                            nY = 0
                                            while nY < 10:
                                                
                                                if nY != aY:
                                                    extendedHorrorForecastDisplay.set(anX, nY, "\r")
                                                    
                                                nY = nY + 1
                                            
                                            ig = ig + 1
                                        
                                        def _getHallowColor(aValue, invert=False):
                                            if aValue > 0:
                                                if invert:
                                                    return "magenta"
                                                return "red"
                                            elif aValue > -5:
                                                if invert: 
                                                    return "blue"
                                                return "light_red"
                                            elif aValue > -10:
                                                if invert: 
                                                    return "light_blue"
                                                return "yellow"
                                            elif aValue > -20:
                                                if invert: 
                                                    return "cyan"
                                                return "light_yellow"
                                            else:
                                                if section == "Uncanny Phase":
                                                    if invert:
                                                        return "cyan"
                                                    return "light_yellow"
                                                else:
                                                    if invert:
                                                        return "light_cyan"
                                                    return "light_green"
                                            
                                        printColor(50, globals.maxY - 13, str(round(minValue, 2))[0:4] + (" " * (len(str(round(minValue, 2))) < 4)) + " : " + horrorForecastDisplay.data[9], _getHallowColor(minValue))
                                        printColor(50, globals.maxY - 14, str(round(minValue + (stepValue), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue), 2))) < 4)) + " : " + horrorForecastDisplay.data[8], _getHallowColor(minValue + (stepValue)))
                                        printColor(50, globals.maxY - 15, str(round(minValue + (stepValue * 2), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue * 2), 2))) < 4)) + " : " + horrorForecastDisplay.data[7], _getHallowColor(minValue + (stepValue * 2)))
                                        printColor(50, globals.maxY - 16, str(round(minValue + (stepValue * 3), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue * 3), 2))) < 4)) + " : " + horrorForecastDisplay.data[6], _getHallowColor(minValue + (stepValue * 3)))
                                        printColor(50, globals.maxY - 17, str(round(minValue + (stepValue * 4), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue * 4), 2))) < 4)) + " : " + horrorForecastDisplay.data[5], _getHallowColor(minValue + (stepValue * 4)))
                                        printColor(50, globals.maxY - 18, str(round(minValue + (stepValue * 5), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue * 5), 2))) < 4)) + " : " + horrorForecastDisplay.data[4], _getHallowColor(minValue + (stepValue * 5)))
                                        printColor(50, globals.maxY - 19, str(round(minValue + (stepValue * 6), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue * 6), 2))) < 4)) + " : " + horrorForecastDisplay.data[3], _getHallowColor(minValue + (stepValue * 6)))
                                        printColor(50, globals.maxY - 20, str(round(minValue + (stepValue * 7), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue * 7), 2))) < 4)) + " : " + horrorForecastDisplay.data[2], _getHallowColor(minValue + (stepValue * 7)))
                                        printColor(50, globals.maxY - 21, str(round(minValue + (stepValue * 8), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue * 8), 2))) < 4)) + " : " + horrorForecastDisplay.data[1], _getHallowColor(minValue + (stepValue * 8)))
                                        printColor(50, globals.maxY - 22, str(round(minValue + (stepValue * 9), 2))[0:4] + (" " * (len(str(round(minValue + (stepValue * 9), 2))) < 4)) + " : " + horrorForecastDisplay.data[0], _getHallowColor(minValue + (stepValue * 9)))

                                        printColor(45, globals.maxY - 13, str(round(extendedMinValue, 2))[0:4] + (" " * (len(str(round(extendedMinValue, 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[9][0 + (4 * (_getHallowColor(extendedMinValue, invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue, invert=True))
                                        printColor(45, globals.maxY - 14, str(round(extendedMinValue + (extendedStepValue), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[8][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue), invert=True))
                                        printColor(45, globals.maxY - 15, str(round(extendedMinValue + (extendedStepValue * 2), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue * 2), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[7][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue * 2), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue * 2), invert=True))
                                        printColor(45, globals.maxY - 16, str(round(extendedMinValue + (extendedStepValue * 3), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue * 3), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[6][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue * 3), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue * 3), invert=True))
                                        printColor(45, globals.maxY - 17, str(round(extendedMinValue + (extendedStepValue * 4), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue * 4), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[5][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue * 4), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue * 4), invert=True))
                                        printColor(45, globals.maxY - 18, str(round(extendedMinValue + (extendedStepValue * 5), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue * 5), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[4][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue * 5), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue * 5), invert=True))
                                        printColor(45, globals.maxY - 19, str(round(extendedMinValue + (extendedStepValue * 6), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue * 6), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[3][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue * 6), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue * 6), invert=True))
                                        printColor(45, globals.maxY - 20, str(round(extendedMinValue + (extendedStepValue * 7), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue * 7), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[2][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue * 7), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue * 7), invert=True))
                                        printColor(45, globals.maxY - 21, str(round(extendedMinValue + (extendedStepValue * 8), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue * 8), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[1][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue * 8), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue * 8), invert=True))
                                        printColor(45, globals.maxY - 22, str(round(extendedMinValue + (extendedStepValue * 9), 2))[0:4] + (" " * (len(str(round(extendedMinValue + (extendedStepValue * 9), 2))) < 4)) + "\r\r\r" + extendedHorrorForecastDisplay.data[0][0 + (4 * (_getHallowColor(extendedMinValue + (extendedStepValue * 9), invert=True) in ["light_blue", "light_cyan"])):], _getHallowColor(extendedMinValue + (extendedStepValue * 9), invert=True))

                                        ig = 0
                                        minf = pytools.clock.getDateTime()[4]
                                        timecardString = ""
                                        while ig < 20:
                                            if minf < 10:
                                                strminf = " 0" + str(minf)
                                            else:
                                                strminf = " " + str(minf)
                                            timecardString = timecardString + strminf
                                            
                                            ig = ig + 1
                                            minf = minf + 3
                                            if minf >= 60:
                                                minf = minf - 60
                                                
                                        ig = 0
                                        il = 0
                                        hourf = pytools.clock.getDateTime()[2] * 24 + pytools.clock.getDateTime()[3]
                                        monthf = pytools.clock.getDateTime()[1]
                                        extendedTimecardString = ""
                                        extendedDaycardString = ""
                                        firstDayIter = True
                                        lastDay = int(math.floor(hourf / 24))
                                        while ig < (15 + (15 * globals.forecastLength)):
                                            if hourf < 10:
                                                strminf = " 00" + str(hourf)
                                            elif hourf < 100:
                                                strminf = " 0" + str(hourf)
                                            else:
                                                strminf = " " + str(hourf)
                                            extendedTimecardString = extendedTimecardString + strminf
                                            
                                            if int(math.floor(hourf / 24)) != lastDay:
                                                if firstDayIter:
                                                    extendedDaycardString = " " * il
                                                    firstDayIter = False
                                                extendedDaycardString = extendedDaycardString + str(int(math.floor(hourf / 24))) + (" " * (12 - len(str(int(math.floor(hourf / 24))))))
                                                lastDay = int(math.floor(hourf / 24))
                                            ig = ig + 1
                                            hourf = hourf + 8
                                            il = il + 4
                                            if hourf >= pytools.clock.getMonthEnd(monthf) * 24:
                                                hourf = hourf - (pytools.clock.getMonthEnd(monthf) * 24)
                                                monthf = monthf + 1
                                                if monthf > 12:
                                                    monthf = monthf - 12

                                        printColor(50, globals.maxY - 11, "time :" + timecardString, _getHallowColor(horrorForecast[2]))
                                        printColor(45, globals.maxY - 24, "hour      :" + extendedTimecardString, _getHallowColor(extendedHorrorForecast[2], invert=True))
                                        printColor(45, globals.maxY - 25, "^day      :" + extendedDaycardString, _getHallowColor(extendedHorrorForecast[2], invert=True))
                                        
                                        printColor(50, globals.maxY - 28, "Horror Forecast", hallowColor)
                                        printColor(50, globals.maxY - 27, "---------------", hallowColor)
                                        
                                        
                                    if flags.webMode:
                                        
                                        webModeDeathString = ""
                                        
                                        webModeDeathString = webModeDeathString + "DEATH NIGHT ACTIVITY"
                                        webModeDeathString = webModeDeathString + "\n" + "--------------------"
                                        webModeDeathString = webModeDeathString + "\n" + "Horror Index        : " + pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\horrorIndex.cx", False) + "Hi" + spaces[0:10]
                                        try:
                                            webModeDeathString = webModeDeathString + "\n" + "Whispering Index    : " + str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["whisperIndex"]) + "Hi" + spaces[0:10]
                                        except:
                                            webModeDeathString = webModeDeathString + "\n" + "Whispering Index    : " + "0" + "Hi" + spaces[0:10]
                                        try:
                                            webModeDeathString = webModeDeathString + "\n" + "Hallowed Wolf Index : " + str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["hallowedWolfIndex"]) + "Hi" + spaces[0:10]
                                        except:
                                            webModeDeathString = webModeDeathString + "\n" + "Hallowed Wolf Index : " + "0" + "Hi" + spaces[0:10]
                                        webModeDeathString = webModeDeathString + "\n" + "Current Section     : " + section + spaces[0:10]
                                        pytools.IO.saveFile(flags.webMode + "\\deathMode.txt", webModeDeathString)
                                else:
                                    pytools.IO.saveFile(flags.webMode + "\\deathMode.txt", "")
                            else:
                                pytools.IO.saveFile(flags.webMode + "\\deathMode.txt", "")
                        except:
                            # print(traceback.format_exc())            
                            # print(aY)
                            pass
                    except:
                        pass
                else:
                    system.status.active = False
                if flash == 0:
                    flash = 1
                else:
                    flash = 0
                printColor(0, globals.maxY - 1, "(m &+ enter) - Goto Menu, (t &+ toggle 5/10 day forecast)", "green")
                
            time.sleep(0.3)
    except:
        print(traceback.format_exc())
        flags.exitf = True
        
startf = False
runf = False
stopf = False
en = True
try:
    for n in sys.argv:
        print(n)
        if runf:
            if n == "--start":
                startf = True
            elif n == "--stop":
                stopf = True
            elif n.split("=")[0] == "--apiKey":
                flags.apiKey = n.split("=")[1]
            elif n.split("=")[0] == "--remote":
                flags.remote = n.split("=")[1]
            elif n.split("=")[0] == "--webMode":
                flags.webMode = n.split("=")[1]
            elif n == "--startDefault":
                flags.defaultSystemState = True
            elif n == "--server":
                flags.server = True
            elif n =="--noDisplay":
                flags.displayOnScreen = False
            elif n == "--monitor":
                flags.monitor = True
            elif n == "--update":
                flags.update = True
            elif n == "--restart":
                flags.restart = True
            elif n == "--noUnpack":
                flags.unpack = False
            elif n == "--takeOver":
                flags.bypass = True
            elif n == "--ping":
                print("ping")
            elif n == "--help":
                pass
            else:
                print("Invalid Syntax. Type --help for more options.")
                en = False
        if n == "--run":
            runf = True
        
        if n == "--test":
            tools.max_window()
            time.sleep(1)
            printColor(10, 10, "hello fuck tard!", "red")
            printColor(10, 10, "eat\r\r\r\r\r\r\r\r\rpant", "green")    

        if n == "--help":
            print("Ghosts Ambience System Console Usage")
            print("------------------------------------")
            print("--run: Start the console (must be first always to run command line)")
            print("--start: Start the system automatically upon console load.")
            print("   ^ --apiKey=<apiKey>: must be specified api key on launch.")
            print("                        This will be your Open Weather Map API Key.")
            print("--remote=<remoteIp>: Connects in with a remote ambience server (file sharing must be enabled.)")
            print("   ^ --startDefault: If connection is lost, automatically restart system if it is offline.")
            print("--server: no gui (does not load console window/menu, simply runs the command.")
            print("--monitor: Put's Console into monitor mode.")
            print("   ^ --takeOver: Tells the console to take control,")
            print("                 overriding all other consoles (used for remoting in to manage).")
            print("                 (Requires login credentials of the windows os user.)")
            print("--update: Updates the system.")
            print("   ^ --restart: Performs restart cycle after update. Use if the server in already online.")
            print("   ^ --noUnpack: disables the rerun of setup.py.")
            print("--webMode=<location>: Tees console output to files in folder.")
            print("--noDisplay: Doesn't print output onto screen, only monitors.")
            print("--help: Print this help text.")
except:
    print("Unexpected error:", sys.exc_info())

if flags.remote != False:
    en = comm.connect(en)
    if en:
        pass
        os.chdir("\\\\" + flags.remote + "\\ambience")

if stopf:
    if en:
        system.stop()
        
if flags.update == True:
    if en:
        if flags.restart == True:
            system.update(True)
        else:
            system.update()

if startf:
    if en:
        system.start()
                            
if runf:
    if en:
        if flags.server == False:            
            tools.max_window()
            time.sleep(1)
            thread0 = threading.Thread(target=main)
            thread0.start()
            
            if not flags.webMode:
                thread1 = threading.Thread(target=menu.handler)
                thread1.start()