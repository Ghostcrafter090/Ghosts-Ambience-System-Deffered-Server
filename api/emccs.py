import modules.audio as audio
import modules.pytools as pytools
import time
import os

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }

def getOutStatus():
    out = 0
    if os.path.isfile('nomufflewn.derp') == True:
        out = 1
    return out

def getTestStatus():
    out = 0
    if os.path.isfile('testemccs.derp') == True:
        out = 1
    return out

def main():
    startBool = 0
    while not status.exit:
        time.sleep(1)
        dateArray = pytools.clock.getDateTime()
        if dateArray[1] == 12:
            if getTestStatus() == 1:
                startBool = 0
            if ((dateArray[2] == 24) and (dateArray[3] > 8)) or ((dateArray[2] == 25) and (dateArray[3] < 10)):
                if startBool != 1:
                    try:
                        os.system('del testemccs.derp /f /q')
                    except:
                        pass
                    
                    audio.playSoundAll("emcc-test.mp3", 20, 1, 0, 1)
                    startBool = 1
                if dateArray[3] == 10:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw1.mp3", 3, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 11:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw2.mp3", 6, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 12:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw3.mp3", 9, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 13:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw4.mp3", 12, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 14:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw5.mp3", 15, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 15:
                    if dateArray[4] == 0:
                        audio.playSoundAll("s1_all.mp3", 35, 1, 0, 1)
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s2_window.mp3;s2_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s2_wall.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s2_wall.mp3", 1, 70, 1, 0, 0)
                        audioEvent.register("s2_wall.mp3", 7, 70, 1, 0, 1)
                        audioEvent.run()
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s3_window.mp3;s3_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s3_wall.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s3_wall.mp3", 1, 70, 1, 0, 0)
                        audioEvent.register("s3_wall.mp3", 7, 70, 1, 0, 1)
                        audioEvent.run()
                        
                if dateArray[3] == 16:
                    if dateArray[4] == 20:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s4_window.mp3;s4_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s4_clock.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s4_fireplace.mp3", 1, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s4_generic.mp3", 7, 70, 1, 0, 1, clock=False)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 17:
                    if dateArray[4] == 40:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s5_window.mp3;s5_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s5_clock.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s5_fireplace.mp3", 1, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s5_generic.mp3", 7, 70, 1, 0, 1, clock=False)
                        audioEvent.run()
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s6_window.mp3;s6_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s6_clock.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s6_fireplace.mp3", 1, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s6_generic.mp3", 7, 70, 1, 0, 1, clock=False)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 18:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s7_window.mp3;s7_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s7_clock.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s7_fireplace.mp3", 1, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s7_generic.mp3", 7, 70, 1, 0, 1, clock=False)
                        audioEvent.run()
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s8_window.mp3;s8_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s8_wall.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s8_wall.mp3", 1, 70, 1, 0, 0)
                        audioEvent.register("s8_wall.mp3", 7, 70, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 18:
                    if dateArray[4] == 10:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s9_window.mp3;s9_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s9_clock.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s9_fireplace.mp3", 1, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s9_generic.mp3", 7, 70, 1, 0, 1, clock=False)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 18:
                    if dateArray[4] == 30:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s10_window.mp3;s10_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s10_wall.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s10_wall.mp3", 1, 70, 1, 0, 0)
                        audioEvent.register("s10_wall.mp3", 7, 70, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 21:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s11_window.mp3;s11_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s11_wall.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s11_wall.mp3", 1, 70, 1, 0, 0)
                        audioEvent.register("s11_wall.mp3", 7, 70, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 22:
                    if dateArray[4] == 30:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s12_window.mp3;s12_outside.mp3", 70, 1, 0, 0)
                        audioEvent.register("s12_wall.mp3", 0, 70, 1, 0, 0, clock=False)
                        audioEvent.register("s12_wall.mp3", 1, 70, 1, 0, 0)
                        audioEvent.register("s12_wall.mp3", 7, 70, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  1:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s12.5_window.mp3;s12.5.mp3", 70, 1, 0, 0)
                        audioEvent.register("s12.5_inside.mp3", 0, 70, 1, 0, 0)
                        audioEvent.register("s12.5_inside.mp3", 1, 70, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  1:
                    if dateArray[4] == 20:
                        audio.playSoundAll("s13.mp3", 70, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] ==  1:
                    if dateArray[4] == 30:
                        audio.playSoundAll("s14.mp3", 70, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] ==  1:
                    if dateArray[4] == 50:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s15_window.mp3;s15.mp3", 70, 1, 0, 0)
                        audioEvent.register("s15_inside.mp3", 0, 70, 1, 0, 0)
                        audioEvent.register("s15_inside.mp3", 1, 70, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  2:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s16_window.mp3;s16.mp3", 70, 1, 0, 0)
                        audioEvent.register("s16_fireplace.mp3", 1, 70, 1, 0, 0)
                        audioEvent.register("s16_clock.mp3", 0, 70, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  2:
                    if dateArray[4] == 20:
                        audio.playSoundAll("s17.mp3", 70, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] ==  2:
                    if dateArray[4] == 40:
                        audio.playSoundAll("s18.mp3", 70, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] ==  3:
                    if dateArray[4] == 0:
                        audio.playSoundAll("s19.mp3", 70, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] ==  3:
                    if dateArray[4] == 25:
                        audio.playSoundAll("s20.mp3", 70, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] ==  3:
                    if dateArray[4] == 45:
                        audio.playSoundAll("s21.mp3", 70, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] ==  4:
                    if dateArray[4] == 0:
                        audio.playSoundAll("s22.mp3", 70, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] ==  8:
                    if dateArray[4] == 0 :
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s23_window.mp3;s23.mp3", 70, 1, 0, 0)
                        audioEvent.register("s23_fireplace.mp3", 1, 70, 1, 0, 0)
                        audioEvent.register("s23_clock.mp3", 0, 70, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
