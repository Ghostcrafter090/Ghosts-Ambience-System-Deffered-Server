import modules.audio as audio
import psutil
import time
import sys
import modules.pytools as pytools

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }

def getFile(path):
    error = 0
    try:
        file = open(path, "r")
        jsonData = file.read()
        file.close()
    except:
        print("Unexpected error:", sys.exc_info())
        error = 1
    if error != 0:
        jsonData = error
    return jsonData

def saveFile(path, jsonData):
    error = 0
    try:
        file = open(path, "w")
        file.write(jsonData)
        file.close()
    except:
        print("Unexpected error:", sys.exc_info())
        error = 1
    return error

def getProcesses():
    window = []
    clock = []
    fireplace = []
    outside = []
    windown = []
    windownI = 0
    outsideI = 0
    windowI = 0
    clockI = 0
    fireplaceI = 0
    for proc in psutil.process_iter():
            # Get process name & pid from process object.
            try:
                processName = proc.name()
                processID = proc.cmdline()
                if processName == "window.exe":
                    windowI = windowI + 1
                    window.append(processID)
                if processName == "clock.exe":
                    clockI = clockI + 1
                    clock.append(processID)
                if processName == "fireplace.exe":
                    fireplaceI = fireplaceI + 1
                    fireplace.append(processID)
                if processName == "outside.exe":
                    outsideI = outsideI + 1
                    outside.append(processID)
                if processName == "windown.exe":
                    windownI = windownI + 1
                    windown.append(processID)
            except:
                pass
    return {"clock": clock, "fireplace": fireplace, "window": window, "outside": outside, "windown": windown}

def makeString(listf):
    string = "\n"
    i = 0
    while i < len(listf):
        if listf[i][1] == "runaudio.vbs":
            if string.find("\n" + listf[i][2].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n") == -1:
                string = string + listf[i][2].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n"
        else:
            if string.find("\n" + listf[i][1].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n") == -1:
                string = string + listf[i][1].replace(".mp3", "").replace(".vbs", "").replace("_", " ").replace("active ghost.", "g_") + "\n"
        i = i + 1
    return string[1:]

def main():
    while not status.exit:
        clocksounds = ""
        windowsounds = ""
        fireplacesounds = ""
        outsidesounds = ""
        windownsounds = ""
        processes = getProcesses()
        clocksounds = makeString(processes['clock'])
        fireplacesounds = makeString(processes['fireplace'])
        windowsounds = makeString(processes['window'])
        outsidesounds = makeString(processes['outside'])
        windownsounds = makeString(processes['windown'])
        try:
            newSystem = pytools.IO.getJson("..\\vars\\sounds.json")
            clocksounds = clocksounds + newSystem["clock"]
            fireplacesounds = fireplacesounds + newSystem["fireplace"]
            windowsounds = windowsounds + newSystem["window"]
            outsidesounds = outsidesounds + newSystem["outside"]
        except:
            pass
        windowsounds = windowsounds + windownsounds
        outsidesounds = outsidesounds + windownsounds
        saveFile("..\\vars\\sounds\\clock.cxl", clocksounds)
        saveFile("..\\vars\\sounds\\fireplace.cxl", fireplacesounds)
        saveFile("..\\vars\\sounds\\window.cxl", windowsounds)
        saveFile("..\\vars\\sounds\\outside.cxl", outsidesounds)
        time.sleep(1)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
    
                
