import modules.audio as audio
import modules.pytools as pytools
import os
import time
import psutil
import voicemeeter
import sounddevice as sd  
import time

class globals:
    instance = False
    mme = 2048
    wdm = 1024
    noChange = True
    started = False

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }
    
class tools:
    def getDeviceList():
        xml = pytools.IO.getXml(pytools.IO.getJson("..\server.json")["vmSettings"])
        typef = {
            "1": "mme",
            "4": "wdm"
        }
        out = {
            "inputs": {
                "mme": [],
                "wdm": []
            },
            "outputs": {
                "mme": [],
                "wdm": []
            }
        }
        # Outputs xml['VBAudioVoicemeeterSettings']['VoiceMeeterDeviceConfiguration']['OutputDev']
        # Inputs xml['VBAudioVoicemeeterSettings']['VoiceMeeterDeviceConfiguration']['InputDev']
        for n in xml['VBAudioVoicemeeterSettings']['VoiceMeeterDeviceConfiguration']['OutputDev']:
            try:
                out["outputs"][typef[n['@type']]].append(n["@name"])
            except:
                pass
        for n in xml['VBAudioVoicemeeterSettings']['VoiceMeeterDeviceConfiguration']['InputDev']:
            try:
                out["inputs"][typef[n['@type']]].append(n["@name"])
            except:
                pass
        return out
    
    def getFapIndex(nf):
        out = 0
        i = 0
        while i < (len(nf) - 1):
            out = out + nf[i + 1] - nf[i]
            i = i + 1
        return out / i
        
class audio:
    class devices:
        rec = False
        comp = False
        
        recData = []
        compData = []
        
        def runRec():
            audio.devices.rec.default.device = [4, 4]
            audio.devices.recData = audio.record(audio.devices.rec, 1)
        
        def runComp():
            audio.devices.compData = audio.record(audio.devices.comp, 1)
    
    def timer(duration):
        while duration: 
            mins, secs = divmod(duration, 60) 
            timer = f"{mins} mins:{secs} seconds Left"
            print(timer, end=" \r") 
            time.sleep(1) 
            duration -= 1
    
    def record(sd, duration):
        fs=8120  #frames per second
        print("Recording..........")
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        audio.timer(duration)    #call timer function
        sd.wait()
        return myrecording
    
    def check(ntype):
        audio.devices.comp = sd
        audio.devices.runComp()
        j = 0
        k = True
        x = []
        for n in audio.devices.compData.tolist():
            if n == [0, 0]:
                if k:
                    x.append(j)
                    k = False
            else:
                k = True
            j = j + 1
        print(x)
        oldmme = globals.mme
        oldwdm = globals.wdm
        if (8128 / 6) > len(x) > 30:
            if tools.getFapIndex(x) < 50:
                if ntype == 0:
                    globals.mme = globals.mme + 16
                else:
                    globals.wdm = globals.wdm + 8
                globals.started = True
        else:
            if ((pytools.clock.getDateTime()[4] % 10) == 0) or (globals.started == False):
                if globals.started == False:
                    globals.mme = globals.mme - 128
                    globals.wdm = globals.wdm - 64
                if globals.noChange:
                    globals.mme = globals.mme - 64
                    globals.wdm = globals.wdm - 32
                    globals.noChange = False
            else:
                globals.noChange = True
        if globals.mme < 144:
            globals.mme = 144
        if globals.wdm < 144:
            globals.wdm = 144
        if globals.mme > 2048:
            globals.mme = 2048
        if globals.wdm > 2048:
            globals.wdm = 2048
        if (oldmme != globals.mme) or (oldwdm != globals.wdm):
            globals.instance.set("option.buffer.mme", globals.mme)
            globals.instance.set("option.buffer.wdm", globals.wdm)
            globals.instance.restart()
            return True
        return False

class vm:
    def checkStatus():
        try:
            globals.instance.get("option.buffer.mme")
        except:
            vm.launch()
            globals.instance = voicemeeter.remote("potato")
            globals.instance.login()
        
    def launch():
        if os.path.exists("C:\Program Files (x86)\VB\Voicemeeter\\voicemeeter8.exe"):
            if os.path.exists("..\..\Voicemeeter.lnk"):
                if ("voicemeeter8.exe" in (p.name() for p in psutil.process_iter())) == False:
                    os.system("taskkill /f /im voicemeeter8.exe")
                    os.system('start /b "" ..\..\Voicemeeter.lnk')
        time.sleep(5)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
        
def main():
    blacklist = []
    indexs = {
        "mme": [],
        "wdm": []
    }
    devices = tools.getDeviceList()
    for n in sd.query_devices():
        for g in devices["inputs"]["mme"]:
            if n["name"] == g:
                indexs["mme"].append(n["index"])
        for g in devices["outputs"]["mme"]:
            if n["name"] == g:
                indexs["mme"].append(n["index"])
        for g in devices["inputs"]["wdm"]:
            if n["name"] == g:
                indexs["wdm"].append(n["index"])
        for g in devices["outputs"]["wdm"]:
            if n["name"] == g:
                indexs["wdm"].append(n["index"])
    n = 0
    j = 0
    while not status.exit:
        # vm.checkStatus()
        time.sleep(10)
        if False:
            for n in indexs["mme"]:
                sd.default.device = [n, n]
                vm.checkStatus()
                if (n in blacklist) == False:
                    try:
                        print("Checking device " + sd.query_devices()[n]["name"] + " on interface mme...")
                        if audio.check(0):
                            time.sleep(5)
                            j = 0
                    except:
                        blacklist.append(n)
            for n in indexs["wdm"]:
                sd.default.device = [n, n]
                vm.checkStatus()
                if (n in blacklist) == False:
                    try:
                        print("Checking device " + sd.query_devices()[n]["name"] + " on interface wdm...")
                        if audio.check(1):
                            time.sleep(5)
                            j = 0
                    except:
                        blacklist.append(n)
            if j > 3:
                time.sleep(60)
                j = 0
            else:
                j = j + 1
        

def run():
    status.hasExited = False
    main()
    status.hasExited = True
