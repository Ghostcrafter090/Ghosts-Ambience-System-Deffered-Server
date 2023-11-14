try:
    import modules.pytools as pytools
except:
    import pytools
import time
import os
import termcolor
import sys
import threading
import ctypes
import msvcrt
import subprocess

import urllib.parse
import json
import random

def getNewJson(path, doPrint=True):
    import traceback
    error = 0
    try:
        if path[0:2] == "\\\\":
            jsonData = pytools.net.getJsonAPI("http://" + flags.remote + ":" + str(random.randint(6000, 6029)) + "?json=" + urllib.parse.quote(json.dumps({
                "command": "getJson",
                "data": {
                    "path": ".\\" + path.split("\\ambience\\")[1]
                }
            })))["data"]
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
    return jsonData

def getMultiFile(listf, doPrint=False):
    try:
        return pytools.net.getJsonAPI("http://" + flags.remote + ":" + str(random.randint(6000, 6029)) + "?json=" + urllib.parse.quote(json.dumps({
            "command": "getMultiFile",
            "data": {
                "list": listf.values()
            }
        })))["data"]
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
    timeout = 1000
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
            if (pytools.clock.getDateTime()[5] % 30) == 0:
                try:
                    subprocess.getstatusoutput("net start w32time")
                    subprocess.getstatusoutput("w32tm /resync")
                except:
                    pass
            if f:
                error = subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "choice /c m /n")[0]
            f = True
            # subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "mode con cols=200 lines=63")
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
                        # print(os.listdir())
                        # print(os.listdir(".\\working"))
                        # print(".\\working\\plugin." + plugin + ".run()_errorlog.log")
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
    subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "color")[0]
    pytools.IO.console.printAt(x, y, termcolor.colored(text, color))

spaces = "                                                                    "

def getSection():
    dateArray = pytools.clock.getDateTime()
    dayTimes = pytools.IO.getList(".\\working\\daytimes.pyl", False)[1]
    phases = ["Daylight Phase", "Uncanny Phase", "Dark Phase", "Evil Phase", "Sinister Phase", "Dying Phase P1", "Dying Phase P2", "Dying Phase P3", "Dying Phase P4", "Death Phase", "Necro Phase", "Reserect Phase", "Safe Phase"]
    if pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5]):
        return phases[0]
    else:
        if dateArray[3] > 12:
            if dateArray[3] < 22:
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
            elif dateArray[3] == 22:
                if dateArray[4] < 15:
                    return phases[5]
                if dateArray[4] < 30:
                    return phases[6]
                if dateArray[4] < 45:
                    return phases[7]
                if dateArray[4] >= 45:
                    return phases[8]
            elif dateArray[3] == 23:
                return phases[9]
        elif dateArray[3] < (dayTimes[2][3] - 1):
            return phases[10]
        elif dateArray[3] == (dayTimes[2][3] - 1):
            return phases[11]
        else:
            return phases[12]

def main():
    try:
        i = 0
        # subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "mode con cols=200 lines=63")
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
                            # subprocess.getstatusoutput("echo {\"loopTime\":[9999, 0, 0, 0, 0, 0]} > \\\\" + tools.getRemote() + "\\ambience\\systemLoop.json")[0]
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
                    # subprocess.getstatusoutput("cd \"\\" + tools.getRemote() + "\\ambience\" & " + "mode con cols=200 lines=63")
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
                        pytools.IO.console.printAt(0, 3, weather)
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
                                    pytools.IO.console.printAt(2, i, plugin.split("_keys")[0][0:19])
                                pInfo = outList[".\\vars\\pluginVarsJson\\" + plugin]
                                if system.status.active == True:
                                    if flags.displayOnScreen:
                                        if (os.path.exists(".\\vars\\plugins\\plugin." + plugin.split("_keys")[0] + ".run()-error.cx")) and (".\\vars\\plugins\\plugin." + plugin.split("_keys")[0] + ".run()-error.cx" in outErrorList):
                                            pError = outErrorList[".\\vars\\plugins\\plugin." + plugin.split("_keys")[0] + ".run()-error.cx"]
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
                                            printColor(37, i, " ;;; " + pError, "yellow")
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
                        soundsClock = pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\sounds\\clock.cxl", False).split("\n")
                        soundsFireplace = pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\sounds\\fireplace.cxl", False).split("\n")
                        soundsOutside = pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\sounds\\outside.cxl", False).split("\n")
                        soundsWindow = pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\sounds\\window.cxl", False).split("\n")
                    except:
                        pass
                    
                    try:
                        if flags.displayOnScreen:
                            pytools.IO.console.printAt(50, 0, "Clock Speaker Sounds")
                            pytools.IO.console.printAt(50, 1, "--------------------")
                        fileOutput = ""
                        i = 3
                        for f in soundsClock:
                            if system.status.active == True:
                                if flags.displayOnScreen:
                                    pytools.IO.console.printAt(50, i, f + spaces[len(f):30])
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
                        if flags.displayOnScreen:
                            pytools.IO.console.printAt(80, 0, "Fireplace Speaker Sounds")
                            pytools.IO.console.printAt(80, 1, "------------------------")
                        fileOutput = ""
                        i = 3
                        for f in soundsFireplace:
                            if system.status.active == True:
                                if flags.displayOnScreen:
                                    pytools.IO.console.printAt(80, i, f + spaces[len(f):30])
                                fileOutput = fileOutput + "\n" + f + spaces[len(f):30]
                                i = i + 1
                        if flags.webMode:
                            pytools.IO.saveFile(flags.webMode + "\\fireplaceSounds.txt", fileOutput)
                        if flags.displayOnScreen:
                            f = i
                            while i < (f + 10):
                                pytools.IO.console.printAt(80, i, spaces[0:30])
                                i = i + 1
                    except:
                        pass
                    
                    try:
                        if flags.displayOnScreen:
                            pytools.IO.console.printAt(110, 0, "Window Speaker Sounds")
                            pytools.IO.console.printAt(110, 1, "--------------------")
                        fileOutput = ""
                        i = 3
                        for f in soundsWindow:
                            if system.status.active == True:
                                if flags.displayOnScreen:
                                    pytools.IO.console.printAt(110, i, f + spaces[len(f):30])
                                fileOutput = fileOutput + "\n" + f + spaces[len(f):30]
                                i = i + 1
                        if flags.webMode:
                            pytools.IO.saveFile(flags.webMode + "\\windowSounds.txt", fileOutput)
                        if flags.displayOnScreen:
                            f = i
                            while i < (f + 10):
                                pytools.IO.console.printAt(110, i, spaces[0:30])
                                i = i + 1
                    except:
                        pass
                    
                    try:
                        if flags.displayOnScreen:
                            pytools.IO.console.printAt(140, 0, "Outside Speaker Sounds")
                            pytools.IO.console.printAt(140, 1, "--------------------")
                        fileOutput = ""
                        i = 3
                        for f in soundsOutside:
                            if system.status.active == True:
                                if flags.displayOnScreen:
                                    pytools.IO.console.printAt(140, i, f + spaces[len(f):30])
                                fileOutput = fileOutput + "\n" + f + spaces[len(f):30]
                                i = i + 1
                        if flags.webMode:
                            pytools.IO.saveFile(flags.webMode + "\\outsideSounds.txt", fileOutput)
                        if flags.displayOnScreen:
                            f = i
                            while i < (f + 10):
                                pytools.IO.console.printAt(140, i, spaces[0:30])
                                i = i + 1
                    except:
                        pass
                    
                    try:
                        if flags.displayOnScreen:
                            clients = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\hosts.json", doPrint=False)
                            clientsData = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\hostData.json", doPrint=False)
                        
                        if flags.displayOnScreen:
                            pytools.IO.console.printAt(130, globals.maxY - 1, "Ambience Client Information            ")
                            pytools.IO.console.printAt(130, globals.maxY - 2, "---------------------------------------")
                            pytools.IO.console.printAt(130, globals.maxY - 3, " IP            STATUS     MAX CUR OPEN ")
                            pytools.IO.console.printAt(130, globals.maxY - 4, "                                      ")
                        
                        totalSounds = 0
                        maxSounds = 0
                        i = 2
                        if flags.displayOnScreen:
                            for client in clients["hosts"]:
                                try:
                                    pytools.IO.console.printAt(131, globals.maxY - 3 - i, client + "             " + str(int(clientsData[client]["max"]) + 1) + spaces[len(str(int(clientsData[client]["max"]))):3] + " " + str(int(clientsData[client]["current"])) + spaces[len(str(int(clientsData[client]["current"]))):3] + " " + str(clientsData[client]["play"]) + spaces[len(str(clientsData[client]["play"])):5])
                                    if clientsData[client]["current"] > clientsData[client]["max"] + 1:
                                        if flags.displayOnScreen:
                                            printColor(145, globals.maxY - 3 - i, "overload", "red")
                                            if flash == 0:
                                                printColor(130, globals.maxY - 3 - i, "!", "yellow")
                                            else:
                                                printColor(130, globals.maxY - 3 - i, " ", "yellow")
                                    else:
                                        if flags.displayOnScreen:
                                            printColor(130, globals.maxY - 3 - i, " ", "yellow")
                                            printColor(145, globals.maxY - 3 - i, "connected", "green")
                                except:
                                    if flags.displayOnScreen:
                                        pytools.IO.console.printAt(131, globals.maxY - 3 - i, client + "  no data.      ")
                                        if flash == 0:
                                            printColor(130, globals.maxY - 3 - i, "!", "red")
                                        else:
                                            printColor(130, globals.maxY - 3 - i, " ", "red")
                                try:
                                    totalSounds = totalSounds + clientsData[client]["current"]
                                    maxSounds = maxSounds + clientsData[client]["max"]
                                except:
                                    pass
                                i = i + 1
                        
                        if flags.displayOnScreen:
                            try:
                                outsideVolume = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "outsideProperties.json")["volume"]
                                outsideLimiter = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "outsideProperties.json")["limiter"]
                                gilTic = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "gil.json")["prevTic"]
                                gilInterval = pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + "gil.json")["switchInterval"]
                                
                                if flags.displayOnScreen:
                                    pytools.IO.console.printAt(131, globals.maxY - 3 - i - 1, "Outside Volume/Limiter (V / L): " + str(round(outsideVolume, 3)) + "Db / " + str(round(outsideLimiter, 3)) + "Db")
                                    pytools.IO.console.printAt(131, globals.maxY - 3 - i - 2, "GIL Information (prevTic / switchInterval): " + str(round(gilTic, 4)) + " / " + str(gilInterval))
                            except:
                                pass
                            pytools.IO.console.printAt(131, globals.maxY - 3 - i - 3, "Total Sounds: " + str(totalSounds) + " (" + str(int((totalSounds / maxSounds) * 100)) + "% of total)")
                            pytools.IO.console.printAt(130, globals.maxY - 3 - i, "                                      ")

                            i = i + 2
                            fn = i
                            while i < (fn + 10):
                                if flags.displayOnScreen:
                                    pytools.IO.console.printAt(130, globals.maxY - 3 - i - 3, spaces[0:40])
                                i = i + 1
                        # i = 1
                        # while i < 10:
                        #     pytools.IO.console.printAt(140, globals.maxY - len(clients["hosts"]) - len(clients["hosts"]) - len(clients["hosts"]) - i, spaces[0:30])
                        #     i = i + 1
                    except:
                        pass
                        
                    try:
                        if system.status.active == True:
                            if os.path.exists(".\\working\\halloweenmode.derp") or os.path.exists(".\\working\\deathmode.derp"):
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
                                if flags.displayOnScreen:
                                    printColor(50, globals.maxY - 9, "DEATH NIGHT ACTIVITY", "red")
                                    printColor(50, globals.maxY - 8, "--------------------", "red")
                                    printColor(50, globals.maxY - 6, "Horror Index        : " + pytools.IO.getFile("\\\\" + flags.remote + "\\ambience\\" + ".\\working\\horrorIndex.cx", False) + "Hi" + spaces[0:10], "red")
                                    try:
                                        printColor(50, globals.maxY - 5, "Whispering Index    : " + str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["whisperIndex"]) + "Hi" + spaces[0:10], "red")
                                    except:
                                        printColor(50, globals.maxY - 5, "Whispering Index    : " + "0" + "Hi" + spaces[0:10], "red")
                                    try:
                                        printColor(50, globals.maxY - 4, "Hallowed Wolf Index : " + str(pytools.IO.getJson("\\\\" + flags.remote + "\\ambience\\" + ".\\vars\\pluginVarsJson\\deathmode_keys.json", False)["hallowedWolfIndex"]) + "Hi" + spaces[0:10], "red")
                                    except:
                                        printColor(50, globals.maxY - 4, "Hallowed Wolf Index : " + "0" + "Hi" + spaces[0:10], "red")
                                    printColor(50, globals.maxY - 3, "Current Section     : " + section + spaces[0:10], "red")
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
                        pass             
                else:
                    system.status.active = False
                if flash == 0:
                    flash = 1
                else:
                    flash = 0
                printColor(0, globals.maxY - 1, "(m &+ enter) - Goto Menu", "green")
                
            time.sleep(0.3)
    except:
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
            thread1 = threading.Thread(target=menu.handler)
            thread0.start()
            thread1.start()