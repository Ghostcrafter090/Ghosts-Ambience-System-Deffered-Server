import modules.audio as audio
import modules.pytools as pytools
import time
import modules.logManager as log
import random

audioBuffer = audio.rapidFire(10)

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [], [], [], [], [], [], [], [0, 0, 0]]
        return out
    
    def getLightningData():
        try:
            lightningDanger = pytools.IO.getJson("lightningData.json")["dangerLevel"]
            if lightningDanger < 0:
                lightningDanger = 0
        except:
            lightningDanger = 0
        return lightningDanger

class sounds:
    def rain():
        audioEvent = audio.event()
        volume = ((((0.458048 ** ( - 0.670194 * (utils.getLightningData() + 3.94567)) - 7.88269) / 32) + ((100 * utils.dataGrabber()[2][3]) + (100 * utils.dataGrabber()[9][1]) + (100 * utils.dataGrabber()[9][2])) * 0.3) * 7) + 15 + (utils.dataGrabber()[1][0] * 4)
        if volume > 100:
            volume = 100
        print("Playing Rain effect at volume: " + str(volume))
        audioEvent.registerWindow("rain.mp3;rain_nm.mp3", [volume, volume], 1.0, 0.0, 0)
        if utils.getLightningData() > 0:
            hailVolume = ((((0.458048 ** ( - 0.670194 * (utils.getLightningData() + 3.94567)) - 7.88269) / 3) + (100 * utils.dataGrabber()[2][3]) + (100 * utils.dataGrabber()[9][2])) / 3) + utils.dataGrabber()[1][0]
            print("Playing hail effect at volume " + str(hailVolume))
            if hailVolume > 100:
                hailVolume = 100
            audioEvent.registerWindow("hail.mp3;hail_nm.mp3", [hailVolume, hailVolume], 1.0, 0.0, 0)
        audioEvent.register("lightrain_wall.mp3", 0, volume * 1.7, 1.0, 0.0, 0)
        audioEvent.register("lightrain_wall.mp3", 1, volume * 1.7, 1.0, 0.0, 0)
        audioBuffer.registerCombine(audioEvent)

    def lightRain():
        audioEvent = audio.event()
        volume = ((((0.458048 ** ( - 0.670194 * (utils.getLightningData() + 3.94567)) - 7.88269) / 32) + ((100 * utils.dataGrabber()[2][3]) + (100 * utils.dataGrabber()[9][1]) + (100 * utils.dataGrabber()[9][2])) * 0.3) * 7) + 15 + (utils.dataGrabber()[1][0] * 4)
        if volume > 100:
            volume = 100
        print("Playing Light Rain effect at volume: " + str(volume))
        audioEvent.registerWindow("lightrain.mp3;lightrain_nm.mp3", [volume * 1.7, volume * 1.7], 1.0, 0.0, 0)
        audioEvent.register("lightrain_wall.mp3", 0, volume * 1.17, 1.0, 0.0, 0)
        audioEvent.register("lightrain_wall.mp3", 1, volume * 1.17, 1.0, 0.0, 0)
        audioBuffer.registerCombine(audioEvent)
    
    def mist():
        volume = ((((0.458048 ** ( - 0.670194 * (utils.getLightningData() + 3.94567)) - 7.88269) / 32) + ((100 * utils.dataGrabber()[2][3]) + (100 * utils.dataGrabber()[9][1]) + (100 * utils.dataGrabber()[9][2])) * 0.3) * 7) + 15 + (utils.dataGrabber()[1][0] * 4)
        if volume > 100:
            volume = 100
        print("Playing Mist effect at volume: " + str(volume))
        audioBuffer.playSoundWindow("lightrain.mp3;mist_nm.mp3", [volume * 0.85, volume * 1.7], 1.0, 0.0, 0)

def main():
    while not status.exit:
        dataList = utils.dataGrabber()
        if dataList[0][4] == "rain":
            sounds.rain()
        if dataList[0][4] == "lightrain":
            sounds.lightRain()
        if dataList[0][4] == "mist":
            sounds.mist()
        if dataList[0][4] == "thunder":
            if dataList[2][3] > 0:
                sounds.rain()
        time.sleep(194 * (0.2 + random.random()))
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
        
def run():
    status.hasExited = False
    audioBuffer._start()
    main()
    audioBuffer._stop()
    status.hasExited = True
            
        

