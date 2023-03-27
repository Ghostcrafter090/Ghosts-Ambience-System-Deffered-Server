import modules.audio as audio
import modules.pytools as pytools
import time

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
            
        }
    }

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
        volumeGust = (utils.handleComplex(((xGust - 13) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 8) / 0.03) ** (1 / 3)) + 5.5) * 1.5
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
        if volume > 0:
            if status.vars["nextPlays"]["lightChimneyWind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["lightChimneyWind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.register("light_chimney_wind.wav", 1, volume, speed, 0.0, 0)    
                audioEvent.run()
    def lightWind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 9) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 6) / 0.03) ** (1 / 3)) + 5.5) * 1.5
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
        if volume > 0:
            if status.vars["nextPlays"]["lightWind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["lightWind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.register("light_wind.wav", 0, volume, speed, 0.0, 0)
                audioEvent.register("light_wind.wav", 1, volume, speed, 0.0, 0)
                audioEvent.registerWindow("light_wind.wav;light_wind_nm.mp3", [volume, volume * 4], speed, 0.0, 0)
                audioEvent.run()
    
    def wind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 16) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 11) / 0.03) ** (1 / 3)) + 5.5) * 1.5
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
        if volume > 0:
            if status.vars["nextPlays"]["wind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["wind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audio.playSoundWindow("wind.wav;wind_nm.mp3", [volume, volume * 4], speed, 0.0, 0)
    
    def chimneyWind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 24) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 16) / 0.03) ** (1 / 3)) + 5.5) * 1.5
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
        if volume > 0:
            if status.vars["nextPlays"]["chimneyWind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["chimneyWind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.register("chimney_wind.wav", 1, volume, speed, 0.0, 0)
                audioEvent.run()

    def hurricaneWind(xGust, xSpeed):
        volumeGust = (utils.handleComplex(((xGust - 30) / 0.03) ** (1 / 3)) + 5.5) * 1.5
        volumeSpeed = (utils.handleComplex(((xSpeed - 28) / 0.03) ** (1 / 3)) + 5.5) * 1.5
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
        if volume > 0:
            if status.vars["nextPlays"]["hurricaneWind"] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                status.vars["nextPlays"]["hurricaneWind"] = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + (194 / (speed ** 0.5))
                audioEvent = audio.event()
                audioEvent.register("hurricane_wail.mp3", 0, volume, speed, 0.0, 0)
                audioEvent.register("hurricane_wail.mp3", 1, volume, speed, 0.0, 0)
                audioEvent.registerWindow("hurricane_wail.mp3;hurricane_wail_nm.mp3", [volume, volume * 4], speed, 0.0, 0)
                audioEvent.run()

def main():
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
        time.sleep(10)
        status.finishedLoop = True
        status.vars['lastLoop'] = pytools.clock.getDateTime()

def run():
    status.hasExited = False
    main()
    status.hasExited = True
    
    


