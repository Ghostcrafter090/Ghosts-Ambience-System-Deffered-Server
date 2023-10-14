import modules.audio as audio
import modules.pytools as pytools
import time
import modules.logManager as log
import random
import threading

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "nextPlays": {
            "lightWind": 0,
            "lightChimneyWind": 0,
            "wind": 0,
            "chimneyWind": 0,
            "hurricaneWind": 0
        },
        "moodChances": {
            "windMood": 0,
            "flappingFabric": 0,
            "lightWindChime": 0,
            "windChime": 0,
            "chimeIsHung": 0,
            "blowAwayChance": 0,
            "fixCounter": 0
        }
    }
    
class globals:
    windModif = 4.5
    windChime = False
    blowAwayChance = 0
    startHanging = True
    hangThread = False
    fixCounter = 0

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out
    
    def handleComplex(x):
        j = -1.7320508075681864
        if x == complex(x):
            return x.real + (x.imag * j)

class sounds:
    def lightChimneyWind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 13 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 8 + (globals.windModif / 1)) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
            
        volume = volume * 1.85
            
        if volume > 0:
            if status.vars["nextPlays"]["lightChimneyWind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["lightChimneyWind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.register("light_chimney_wind.mp3", 1, volume, speed, 0.0, 0)    
                audioEvent.run()
        
    def lightWind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 9 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 6 + (globals.windModif / 1)) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
            
        volume = volume * 1.6
            
        if volume > 0:
            if status.vars["nextPlays"]["lightWind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["lightWind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.register("light_wind.wav", 0, volume, speed, 0.0, 0)
                audioEvent.register("light_wind.wav", 1, volume, speed, 0.0, 0)
                audioEvent.registerWindow("light_wind.wav;light_wind_nm.mp3", [volume, volume, volume], speed, 0.0, 0)
                audioEvent.register("light_wind.mp3", 9, volume ** 0.8, speed, 0.0, 0)
                audioEvent.run()
                
    def lightWindChimeMood(xGust, xSpeed, getChance=False):
        volumeGust = (utils.handleComplex(((xGust - 8 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 6 + (globals.windModif / 1)) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
            
        volume = volume * 1.6
        
        lightChimeChance = ((volume / 15) ** 2) * 0.21
        if lightChimeChance > 0.21:
            lightChimeChance = 0.21
        if not getChance:
            lightChimeChance = lightChimeChance - sounds.windChimeMood(xGust, xSpeed, getChance=True)
            status.vars["moodChances"]["lightWindChime"] = lightChimeChance
            if random.random() < lightChimeChance:
                if volume > 0:
                    audioEvent = audio.event()
                    audioEvent.register("light_wind_chime.mp3", 9, volume, 1.0, 0.0, 0)
                    audioEvent.register("light_wind_chime.mp3", 3, volume / 5, 1.0, 0.0, 0)
                    audioEvent.register("light_wind_chime.mp3", 2, volume / 5, 1.0, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnFalse, muteFade=True)
                    audioEvent.register("light_wind_chime.mp3", 2, volume / 8, 1.0, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnFalse, muteFade=True, lowPass=300)
                    audioEvent.run()
        else:
            return lightChimeChance
        
    def windCottonMood(xGust, xSpeed, getChance=False):
        volumeGust = (utils.handleComplex(((xGust - 13 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 9 + (globals.windModif / 1)) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
        
        fabricChance = ((volume / 15) ** 2) * 0.7
        status.vars["moodChances"]["flappingFabric"] = fabricChance
        if fabricChance > 1:
            fabricChance = 1
        if not getChance:
            if random.random() < fabricChance:
                if volume > 0:
                    audioEvent = audio.event()
                    audioEvent.register("fabric_flapping.mp3", 9, volume, speed, 0.0, 0)
                    audioEvent.register("fabric_flapping.mp3", 3, volume / 3, speed * 0.8, 0.0, 0)
                    audioEvent.register("fabric_flapping.mp3", 2, volume / 3, speed * 0.8, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnFalse, muteFade=True)
                    audioEvent.register("fabric_flapping.mp3", 2, volume / 5, speed * 0.8, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnTrue, muteFade=True, lowPass=300)
                    audioEvent.run()
        else:
            return fabricChance
        
    def windChimeMood(xGust, xSpeed, getChance=False):
        volumeGust = (utils.handleComplex(((xGust - 11 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 7.5 + (globals.windModif / 1)) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
        
        if volume < 15:
            chimeChance = (((volume / 15) ** 2) * 0.21)
        else:
            chimeChance = (((volume / 15) ** 4) * 0.21)
        
        status.vars["moodChances"]["windChime"] = chimeChance
        if not getChance:
            if random.random() < chimeChance:
                if volume > 0:
                    audioEvent = audio.event()
                    audioEvent.register("wind_chime.mp3", 9, volume, 1.0, 0.0, 0)
                    audioEvent.register("wind_chime.mp3", 3, volume / 5, 1.0, 0.0, 0)
                    audioEvent.register("wind_chime.mp3", 2, volume / 5, 1.0, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnFalse, muteFade=True)
                    audioEvent.register("wind_chime.mp3", 2, volume / 8, 1.0, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnTrue, muteFade=True, lowPass=300)
                    audioEvent.run()
        else:
            return chimeChance
        
    def blowAwayChime(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 16 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 11 + (globals.windModif / 1)) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
            
        globals.blowAwayChance = globals.blowAwayChance + (volume - 15)
        if globals.blowAwayChance < 0:
            globals.blowAwayChance = 0
            
        pytools.IO.saveJson("windChime.json", {
            "is_hung": globals.windChime,
            "wind_metric": globals.blowAwayChance
        })
        
        status.vars["moodChances"]["blowAwayChance"] = globals.blowAwayChance
        status.vars["moodChances"]["chimeIsHung"] = globals.windChime
        
        if globals.blowAwayChance > 10:
            if globals.windChime:
                globals.windChime = False
                audio.playSoundWindow("wind_chime_fall_m.mp3;wind_chime_fall_nm.mp3;wind_chime_fall_nm.mp3", [volume, volume / 2, volume], 1.0, 0.0, 0)
                pytools.IO.saveJson("windChime.json", {
                    "is_hung": globals.windChime,
                    "wind_metric": globals.blowAwayChance
                })
        
    def doSetChimeTrue():
        globals.startHanging = False
        time.sleep(300)
        globals.windChime = True
        globals.startHanging = True
        globals.blowAwayChance = 0
        pytools.IO.saveJson("windChime.json", {
            "is_hung": globals.windChime,
            "wind_metric": globals.blowAwayChance
        })
         
    def hangWindChime(dataList):
        xGust = dataList[0][1]
        xSpeed = dataList[0][0]
        xTemp = dataList[0][7]
        xWeather = dataList[0][4]
        
        if not globals.windChime:
            if globals.startHanging:
                if xGust < (7 + globals.windModif):
                    if xSpeed < (9 + globals.windModif):
                        if xTemp > 15:
                            if (xWeather != "rain") or (xWeather != "lightrain") or (xWeather != "snow") or (xWeather != "thunder"):
                                globals.fixCounter = globals.fixCounter + 1
                                
                                status.vars["moodChances"]["fixCounter"] = globals.fixCounter
                                
                                if globals.fixCounter >= 60:
                                    audioEvent = audio.event()
                                    audioEvent.register("wind_chime_hanging.mp3", 9, 100, 1.0, 0.0, 0)
                                    audioEvent.register("wind_chime_hanging.mp3", 3, 50, 1.0, 0.0, 0)
                                    audioEvent.register("wind_chime_hanging.mp3", 2, 50, 1.0, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnFalse)
                                    audioEvent.register("wind_chime_hanging.mp3", 2, 10, 1.0, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnTrue, lowPass=400)
                                    audioEvent.run()
                                    globals.hangThread = threading.Thread(target=sounds.doSetChimeTrue)
                                    globals.hangThread.start()
                                    globals.fixCounter = 0
                                    status.vars["moodChances"]["fixCounter"] = globals.fixCounter
                        
        
    def windMood(xGust, xSpeed, getChance=False):
        volumeGust = (utils.handleComplex(((xGust - 15 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 10.5 + (globals.windModif / 1)) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
            
        volume = volume * 1.6
        
        moodChance = ((volume / 15) ** 4) * 0.22
        status.vars["moodChances"]["windMood"] = moodChance
        if moodChance > 0.22:
            moodChance = 0.22
        if not getChance:
            if random.random() < moodChance:
                if volume > 0:
                    audioEvent = audio.event()
                    audioEvent.register("wind_mood.mp3", 9, volume, speed, 0.0, 0)
                    audioEvent.register("wind_mood.mp3", 2, volume / 1.2, speed, 0.0, 0, muteFlag="nomufflewn", defaultMuteState=audio.doMuteOnTrue, muteFade=True)
                    audioEvent.register("wind_mood.mp3", 1, volume / 2, speed, 0.0, 0)
                    audioEvent.register("wind_mood.mp3", 0, volume / 4, speed, 0.0, 0)
                    audioEvent.run()
        else:
            return moodChance
    
    def wind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 16 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 11 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
            
        volume = volume * 1.6
        
        if volume > 0:
            if status.vars["nextPlays"]["wind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["wind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.registerWindow("wind.wav;wind_nm.mp3;porch_wind.mp3", [volume, volume, volume], speed, 0.0, 0)
                audioEvent.register("wind_nm.mp3", 9, volume ** 0.9, speed, 0.0, 0)
                audioEvent.run()
    
    def chimneyWind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 24 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 16 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
            
        volume = volume * 1.7
            
        if volume > 0:
            if status.vars["nextPlays"]["chimneyWind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["chimneyWind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.register("chimney_wind.mp3", 1, volume, speed, 0.0, 0)
                audioEvent.run()

    def hurricaneWind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 30 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 28 + globals.windModif) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        if volumeGust > volumeSpeed:
            volume = volumeGust
        else:
            volume = volumeSpeed
        if volume > 10:
            speed = (((volume / 10) - 1) / 4) + 1
        else:
            speed = volume / 10
        if speed < 0.1:
            speed = 0.1
            
        volume = volume * 1.3
            
        if volume > 0:
            if status.vars["nextPlays"]["hurricaneWind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["hurricaneWind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.register("hurricane_wail.mp3", 0, volume, speed, 0.0, 0)
                audioEvent.register("hurricane_wail.mp3", 1, volume, speed, 0.0, 0)
                audioEvent.registerWindow("hurricane_wail.mp3;hurricane_wail_nm.mp3", [volume, volume], speed, 0.0, 0)
                audioEvent.run()

def main():
    
    try:
        globals.windChime = pytools.IO.getJson("windChime.json")["is_hung"]
        globals.blowAwayChance = pytools.IO.getJson("windChime.json")["wind_metric"]
    except:
        pytools.IO.saveJson("windChime.json", {
            "is_hung": False,
            "wind_metric": 0
        })
    
    while not status.exit:
        
        dataList = utils.dataGrabber()
        # if (dataList[0][1] > 13) or (dataList[0][0] > 8):
        sounds.lightChimneyWind(dataList[0][1], dataList[0][0])
        # if (dataList[0][1] > 9) or (dataList[0][0] > 6):
        sounds.lightWind(dataList[0][1], dataList[0][0])
        # if (dataList[0][1] > 16) or (dataList[0][0] > 11):
        sounds.wind(dataList[0][1], dataList[0][0])
        # if (dataList[0][1] > 24) or (dataList[0][0] > 16):
        sounds.chimneyWind(dataList[0][1], dataList[0][0])
        # if (dataList[0][1] > 30) or (dataList[0][0] > 30):
        sounds.hurricaneWind(dataList[0][1], dataList[0][0])
        
        if globals.windChime:
            sounds.lightWindChimeMood(dataList[0][1], dataList[0][0])
            sounds.windChimeMood(dataList[0][1], dataList[0][0])
            sounds.blowAwayChime(dataList[0][1], dataList[0][0])
        else:
            sounds.hangWindChime(dataList)
        
        sounds.windCottonMood(dataList[0][1], dataList[0][0])
        
        sounds.windMood(dataList[0][1], dataList[0][0])
        
        time.sleep(10)
        status.finishedLoop = True
        status.vars['lastLoop'] = pytools.clock.getDateTime()

def run():
    status.hasExited = False
    main()
    status.hasExited = True
    
    


