import modules.pytools as pytools
import threading
import os
import sys
import traceback
import time
import hashlib
import importlib
import modules.defferedTools as defferedTools
import modules.audio as audio
import modules.logManager as log

print = log.printLog

pytools.IO.saveFile(".\\errorlog.log", "")
time.sleep(1)

# pytools.soundEngine.handles.speaker = pytools.soundEngine.speakerPlayer("fireplace", 0, True)

class flags:
    deffered = False

class threads:
    list = {}
    
    def launch(id):
        threads.list[id].start()
    
    def check(id):
        try:
            threads.list[id].join(timeout=0.5)
        except:
            pass
        try:
            if threads.list[id].is_alive():
                print(id)
                out = True
            else:
                out = False
        except:
            return False
        return out
    
class plugin:
    def __init__(self, pluginId, pluginObj, pluginString):
        self.obj = pluginObj
        self.id = pluginId
        self.fileData = pluginString
        
    def run(self):
        while not self.obj.status.exit:
            try:
                if self.id != "old":
                    if self.id != "__pycache__":
                        self.obj.run()
                    else:
                        time.sleep(10)
                else:
                    time.sleep(10)
            except Exception as ex:
                try:
                    handlers.error.log(str(sys.exc_info()[0]), self.id, traceback.format_exc())
                    print(str(sys.exc_info()[0]) + " ;;; " + self.id + " ;;; " + traceback.format_exc())
                    log.write(str(sys.exc_info()[0]) + " ;;; " + traceback.format_exc(), self.id)
                    pytools.IO.saveFile("..\\vars\\plugins\\plugin." + self.id + "-loopStatus.cx", str(traceback.format_exc()))
                    try:
                        self.obj = importlib.reload(self.obj)
                    except:
                        print(traceback.format_exc())
                    time.sleep(3)
                except:
                    print("log error.")
                    time.sleep(3)
    
    obj = False
    id = False
    fileData = ""

class plugins:
    list = {}
    
    def register(name, obj, strf):
        plugins.list[name] = plugin(name, obj, strf)
        
    def load(name):
        threads.list[name] = threading.Thread(target=plugins.list[name].run)
    
class handlers:
    class main:
        
        regObjTemp = {}
        pluginSignature = {}
        
        def registerPlugins():
            os.system("mkdir .\\vars\\plugins")
            pluginsf = os.listdir(".\\api")
            keys = []
            for pluginf in pluginsf:
                print("Importing plugin " + pluginf + "...")
                if pluginf.find(".py") != -1:
                    exec("import api." + pluginf.split(".py")[0] + "\nhandlers.main.regObjTemp['" + pluginf.split(".py")[0] + "'] = api." + pluginf.split(".py")[0])
                    handlers.main.pluginSignature[pluginf.split(".py")[0]] = defferedTools.cipher.hash(pytools.IO.getBytes(".\\api\\" + pluginf))
                    plugins.register(pluginf.split(".py")[0], handlers.main.regObjTemp[pluginf.split(".py")[0]], pytools.IO.getFile(".\\api\\" + pluginf))    
                    keys.append(pluginf.split(".py")[0])
            os.system("del .\\vars\\plugins\\*.cx /f /s /q")
            os.system("del .\\working\\*_errorlog.log")
            pytools.IO.saveFile(".\\vars\\pluginsList.pyn", keys)
            # time.sleep(0.3)
        
        def loadPlugins():
            for pluginf in plugins.list:
                print("Loading plugin " + pluginf + "...")
                plugins.load(pluginf)
                # time.sleep(0.3)
        
        def launchPlugins():
            os.chdir(".\\working")
            for threadf in threads.list:
                print("Launching plugin " + threadf + "...")
                threads.launch(threadf)
                # time.sleep(2)
                
        def activeModify():
            while True:
                for n in os.listdir("..\\api"):
                    try:
                        try:
                            handlers.main.pluginSignature[n.split(".py")[0]]
                        except:
                            handlers.main.pluginSignature[n.split(".py")[0]] = b''
                        if defferedTools.cipher.hash(pytools.IO.getBytes("..\\api\\" + n)) != handlers.main.pluginSignature[n.split(".py")[0]]:
                            plugins.list[n.split(".py")[0]].obj.status.exit = True
                            handlers.error.systemLog("Attempting force stop of plugin...", n)
                            if plugins.list[n.split(".py")[0]].obj.status.hasExited == True:
                                handlers.error.systemLog("Attempting force restart of plugin...", n)
                                log.write("Attempting force restart of plugin...", n)
                                
                                threads.list.pop(n.split(".py")[0])
                                pluginf = n
                                if pluginf.find(".py") != -1:
                                    plugins.list[n.split(".py")[0]].obj = importlib.reload(plugins.list[n.split(".py")[0]].obj)
                                    handlers.main.pluginSignature[pluginf.split(".py")[0]] = defferedTools.cipher.hash(pytools.IO.getBytes("..\\api\\" + n))
                                    # keys.append(pluginf.split(".py")[0])
                                    plugins.load(n.split(".py")[0])
                                    threads.launch(n.split(".py")[0])
                    except:
                        try:
                            if n != "__pycache__":
                                handlers.error.systemLog(traceback.format_exc(), n)
                        except:
                            handlers.error.systemLog(traceback.format_exc())
                time.sleep(5)
                                
    class error:

        errorStatus = {}

        def log(error, pluginf, tracebackf):
            if os.path.isfile(pluginf + '_errorlog.log') == False:
                pytools.IO.saveFile(pluginf + '_errorlog.log', '')
            pytools.IO.saveFile("..\\vars\\plugins\\plugin." + pluginf + ".run()-error.cx", error)
            errorlog = "\n" + str(pytools.clock.getDateTime()) + ' ::: ' + pluginf + "; " + tracebackf
            pytools.IO.appendFile(pluginf + '_errorlog.log', errorlog)
            handlers.error.systemLog(tracebackf, pluginf)
            print("handlers.error.errorStatus['" + pluginf.split(".")[1] + "'] = " + pluginf.replace(".run()", "") + ".status.finishedLoop")
            exec("handlers.error.errorStatus['" + pluginf.split(".")[1] + "'] = " + pluginf.replace(".run()", "") + ".status.finishedLoop")
            pytools.IO.saveFile("..\\vars\\plugins\\" + pluginf + "-loopStatus.cx", str(handlers.error.errorStatus[pluginf.split(".")[1]]))
            
        def systemLog(strf, plugin=False):
            if not plugin:
                print(strf)
            else:
                log.write(strf, plugin)
                print(strf)
            print(str(pytools.clock.getDateTime()) + ' ::: ' + str(plugin) + "; " + strf)

def soundsReporter():
    while False:
        try:
            window = "\n"
            clock = "\n"
            fireplace = "\n"
            outside = "\n"
            try:
                pluginList = os.listdir("..\\vars\\pluginVarsJson")
            except:
                pluginList = os.listdir(".\\vars\\pluginVarsJson")
            i = 0
            while i < len(pluginList):
                pluginf = pluginList[i].split("_keys.json")[0]
                try:
                    try:
                        sounds = plugins.list[pluginf].obj.audio.obj.activeSounds
                    except:
                        sounds = {}
                    try:
                        for n in sounds:
                            print(str(sounds[n][0]) + " " + str(sounds[n][2]) + " " + str(sounds[n][3]))
                            
                            if (pytools.clock.dateArrayToUTC(sounds[n][2]) + sounds[n][3]) > pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                                if sounds[n][1] == "window":
                                    if window.find("\n"+ sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n") == -1:
                                        print(sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_"))
                                        window = window + sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n"
                                elif sounds[n][1] == "clock":
                                    if clock.find("\n"+ sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n") == -1:
                                        print(sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_"))
                                        clock = clock + sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n"
                                elif sounds[n][1] == "fireplace":
                                    if fireplace.find("\n"+ sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n") == -1:
                                        print(sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_"))
                                        fireplace = fireplace + sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n"
                                elif sounds[n][1] == "outside":
                                    if outside.find("\n"+ sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n") == -1:
                                        print(sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_"))
                                        outside = outside + sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n"
                                elif sounds[n][1] == "windown":
                                    if outside.find("\n"+ sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n") == -1:
                                        print(sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_"))
                                        outside = outside + sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n"
                                    if window.find("\n"+ sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n") == -1:
                                        print(sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_"))
                                        window = window + sounds[n][0].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n"
                    except:
                        print(traceback.format_exc())
                except:
                    print(traceback.format_exc())
                i = i + 1
            pytools.IO.saveJson("..\\vars\\sounds.json", {
                "clock": clock,
                "fireplace": fireplace,
                "window": window,
                "outside": outside
            })
        except:
            print(traceback.format_exc())
        time.sleep(1)
       
def run():
    
    noHosts = True
    while noHosts:
        try:
            hosts = pytools.IO.getJson(".\\hosts.json")["hosts"]
            if hosts != []:
                noHosts = False
                break
            else:
                print("No hosts connected. Waiting for connection...")
        except:
            print("Hosts file not found or corrupted. Stack Trace: \n" + traceback.format_exc())
        time.sleep(1)
    
    os.system("del .\\vars\\pluginVarsJson\\*.json /f /q")
    os.system("del .\\vars\\pluginSounds\\*.cx /f /s /q")
    handlers.main.registerPlugins()
    handlers.main.loadPlugins()
    audio.command.sendStop()
    handlers.main.launchPlugins()
    
    if flags.deffered:
        activeModify = threading.Thread(target=handlers.main.activeModify)
        activeModify.start()
    
    soundsReport = threading.Thread(target=soundsReporter)
    soundsReport.start()
    
    while True:
        try:
            i = 0
            for pluginf in plugins.list:
                try:
                    compat = False
                    for n in sys.argv:
                        if n.split("=")[0] == "--apiKey":
                            # pytools.IO.saveFile(".\\access.key", n.split("=")[1])
                            pass
                    pytools.IO.saveJson('..\\vars\\\\pluginVarsJson\\' + pluginf + '_keys.json', plugins.list[pluginf].obj.status.vars)
                except:
                    print(traceback.format_exc())
                i = i + 1
            pytools.IO.saveFile("..\\systemLoop.json", "{\"loopTime\":" + str(pytools.clock.getDateTime()) + "}")
            
            for n in os.listdir("..\\api"):
                if n != "old":
                    if n != "__pycache__":
                        try:
                            pytools.dummyf(plugins.list[n.split(".py")[0]])
                        except:
                            try:
                                error = 0
                                out = True
                                while error < 100:
                                    try:
                                        vars = pytools.IO.getJson("..\\vars\\pluginVarsJson\\" + n.split(".py")[0] + "_keys.json")
                                        if (pytools.clock.dateArrayToUTC(vars["lastLoop"]) + 60) > pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                                            out = False
                                    except:
                                        error = error + 1
                                if out:
                                    os.system("mkdir apiNew")
                                    os.system("xcopy \"..\\api\\" + n + "\" .\\apiNew /c /y")
                                    handlers.error.log("Handler for plugin " + n.split(".py")[0] + " has exited unexpectedly.", n.split(".py")[0], "\nAttempting to relaunch thread...")
                                    try:
                                        exec("import apiNew." + n.split(".py")[0] + "\nhandlers.main.regObjTemp['" + n.split(".py")[0] + "'] = apiNew." + n.split(".py")[0])
                                    except:
                                        print(traceback.format_exc())
                                    os.system("del .\\apiNew\\* /f /s /q")
                                    os.system("rmdir .\\apiNew /s /q")
                                    plugins.register(n.split(".py")[0], handlers.main.regObjTemp[n.split(".py")[0]], pytools.IO.getFile("..\\api\\" + n.split(".py")[0] + ".py"))
                                    handlers.main.pluginSignature[pluginf.split(".py")[0]] = defferedTools.cipher.hash(pytools.IO.getBytes("..\\api\\" + pluginf))
                                    plugins.load(n.split(".py")[0])
                                    threads.launch(n.split(".py")[0])
                            except:
                                pass
        
        except:
            pass
        try:
            time.sleep(1)
        except:
            pass

for arg in sys.argv:
    if arg == "--deffered":
        flags.deffered = True

try:
    run()
except:
    if os.path.exists(".\\working"):
        pytools.IO.saveFile(".\\logs\\system\\crashlog.log", traceback.format_exc())
    else:
        pytools.IO.saveFile("..\\logs\\system\\crashlog.log", traceback.format_exc())

allVars = dir()
for name in allVars:
    myvalue = eval(name)
    try:
        if os.path.exists(".\\working"):
            pytools.IO.appendFile(".\\logs\\system\\crashlog.log", name + ", is" + ", " + type(myvalue) + ", and is equal to " + str(myvalue))
        else:
            pytools.IO.appendFile("..\\logs\\system\\crashlog.log", name + ", is" + ", " + type(myvalue) + ", and is equal to " + str(myvalue))
    except:
        pass