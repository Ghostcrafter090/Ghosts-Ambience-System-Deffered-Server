import modules.audio as audio
import modules.pytools as pytools
import time
import os
import modules.logManager as log

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
    
class globals:
    doSchedualed = False

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
                    
                    # audio.playSoundAll("emcc-test.mp3", 5, 1, 0, 1)
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
                        audioEvent.registerWindow("s2_window_vocals.mp3;s2_outside_vocals.mp3", [100, 35, 50], 1, 0, 0)
                        audioEvent.register("s2_wall_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s2_wall_vocals.mp3", 1, 100, 1, 0, 0)
                        audioEvent.register("s2_wall_vocals.mp3", 7, 100, 1, 0, 1)
                        audioEvent.register("s2_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s2_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s2_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s2_music.mp3", 3, 35, 1, 0, 1)
                        audioEvent.register("s2_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s2_music.mp3", 9, 50, 1, 0, 1)
                        audioEvent.run()
                        
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s3_window_vocals.mp3;s3_outside_vocals.mp3", [100, 35, 50], 1, 0, 0)
                        audioEvent.register("s3_wall_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s3_wall_vocals.mp3", 1, 100, 1, 0, 0)
                        audioEvent.register("s3_wall_vocals.mp3", 7, 100, 1, 0, 1)
                        audioEvent.register("s3_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s3_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s3_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s3_music.mp3", 3, 35, 1, 0, 1)
                        audioEvent.register("s3_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s3_music.mp3", 9, 50, 1, 0, 1)
                        audioEvent.run()
                        
                if dateArray[3] == 16:
                    if dateArray[4] == 20:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s4_window_vocals.mp3;s4_outside_vocals.mp3", [100, 35, 50], 1, 0, 0)
                        audioEvent.register("s4_clock_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s4_fireplace_vocals.mp3", 1, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s4_generic_vocals.mp3", 7, 100, 1, 0, 1, clock=False)
                        audioEvent.register("s4_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s4_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s4_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s4_music.mp3", 3, 35, 1, 0, 1)
                        audioEvent.register("s4_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s4_music.mp3", 9, 50, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 17:
                    if dateArray[4] == 40:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s5_window_vocals.mp3;s5_outside_vocals.mp3", [100, 25, 90], 1, 0, 0)
                        audioEvent.register("s5_clock_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s5_fireplace_vocals.mp3", 1, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s5_generic_vocals.mp3", 7, 100, 1, 0, 1, clock=False)
                        audioEvent.register("s5_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s5_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s5_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s5_music.mp3", 3, 25, 1, 0, 1)
                        audioEvent.register("s5_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s5_music.mp3", 9, 90, 1, 0, 1)
                        audioEvent.run()
                        
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s6_window_vocals.mp3;s6_outside_vocals.mp3", [100, 20, 100], 1, 0, 0)
                        audioEvent.register("s6_clock_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s6_fireplace_vocals.mp3", 1, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s6_generic_vocals.mp3", 7, 100, 1, 0, 1, clock=False)
                        audioEvent.register("s6_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s6_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s6_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s6_music.mp3", 3, 20, 1, 0, 1)
                        audioEvent.register("s6_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s6_music.mp3", 9, 100, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 18:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s7_window_vocals.mp3;s7_outside_vocals.mp3", [100, 100, 70], 1, 0, 0)
                        audioEvent.register("s7_clock_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s7_fireplace_vocals.mp3", 1, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s7_generic_vocals.mp3", 7, 100, 1, 0, 1, clock=False)
                        audioEvent.register("s7_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s7_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s7_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s7_music.mp3", 3, 40, 1, 0, 1)
                        audioEvent.register("s7_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s7_music.mp3", 9, 70, 1, 0, 1)
                        audioEvent.run()
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s8_window_vocals.mp3;s8_outside_vocals.mp3", [100, 35, 60], 1, 0, 0)
                        audioEvent.register("s8_wall_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s8_wall_vocals.mp3", 1, 100, 1, 0, 0)
                        audioEvent.register("s8_wall_vocals.mp3", 7, 100, 1, 0, 1)
                        audioEvent.register("s8_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s8_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s8_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s8_music.mp3", 3, 35, 1, 0, 1)
                        audioEvent.register("s8_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s8_music.mp3", 9, 60, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 18:
                    if dateArray[4] == 10:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s9_window_vocals.mp3;s9_outside_vocals.mp3", [100, 10, 100], 1, 0, 0)
                        audioEvent.register("s9_clock_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s9_fireplace_vocals.mp3", 1, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s9_generic_vocals.mp3", 7, 100, 1, 0, 1, clock=False)
                        audioEvent.register("s9_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s9_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s9_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s9_music.mp3", 3, 35, 1, 0, 1)
                        audioEvent.register("s9_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s9_music.mp3", 9, 100, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 18:
                    if dateArray[4] == 30:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s10_window_vocals.mp3;s10_outside_vocals.mp3", [100, 35, 50], 1, 0, 0)
                        audioEvent.register("s10_wall_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s10_wall_vocals.mp3", 1, 100, 1, 0, 0)
                        audioEvent.register("s10_wall_vocals.mp3", 7, 100, 1, 0, 1)
                        audioEvent.register("s10_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s10_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s10_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s10_music.mp3", 3, 35, 1, 0, 1)
                        audioEvent.register("s10_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s10_music.mp3", 9, 50, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 21:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s11_window_vocals.mp3;s11_outside_vocals.mp3", [100, 20, 60], 1, 0, 0)
                        audioEvent.register("s11_wall_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s11_wall_vocals.mp3", 1, 100, 1, 0, 0)
                        audioEvent.register("s11_wall_vocals.mp3", 7, 100, 1, 0, 1)
                        audioEvent.register("s11_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s11_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s11_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s11_music.mp3", 3, 20, 1, 0, 1)
                        audioEvent.register("s11_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s11_music.mp3", 9, 60, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] == 22:
                    if dateArray[4] == 30:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s12_window_vocals.mp3;s12_outside_vocals.mp3", [100, 20, 50], 1, 0, 0)
                        audioEvent.register("s12_wall_vocals.mp3", 0, 100, 1, 0, 0, clock=False)
                        audioEvent.register("s12_wall_vocals.mp3", 1, 100, 1, 0, 0)
                        audioEvent.register("s12_wall_vocals.mp3", 7, 100, 1, 0, 1)
                        audioEvent.register("s12_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s12_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s12_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s12_music.mp3", 3, 20, 1, 0, 1)
                        audioEvent.register("s12_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s12_music.mp3", 9, 50, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  1:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s12.5_window_vocals.mp3;s12.5_vocals.mp3", [100, 28, 45], 1, 0, 0)
                        audioEvent.register("s12.5_inside_vocals.mp3", 0, 100, 1, 0, 0)
                        audioEvent.register("s12.5_inside_vocals.mp3", 1, 100, 1, 0, 1)
                        audioEvent.register("s12.5_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s12.5_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s12.5_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s12.5_music.mp3", 3, 28, 1, 0, 1)
                        audioEvent.register("s12.5_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s12.5_music.mp3", 9, 45, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  1:
                    if dateArray[4] == 20:
                        audioEvent = audio.event()
                        audioEvent.register("s13.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s13.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s13.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s13.mp3", 3, 20, 1, 0, 1)
                        audioEvent.register("s13.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s13.mp3", 9, 40, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  1:
                    if dateArray[4] == 30:
                        audioEvent = audio.event()
                        audioEvent.register("s14.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s14.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s14.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s14.mp3", 3, 20, 1, 0, 1)
                        audioEvent.register("s14.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s14.mp3", 9, 40, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  1:
                    if dateArray[4] == 50:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s15_window_vocals.mp3;s15_vocals.mp3", [25, 20, 50], 1, 0, 0)
                        audioEvent.register("s15_inside_vocals.mp3", 0, 25, 1, 0, 0)
                        audioEvent.register("s15_inside_vocals.mp3", 1, 25, 1, 0, 1)
                        audioEvent.register("s15_music.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s15_music.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s15_music.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s15_music.mp3", 3, 20, 1, 0, 1)
                        audioEvent.register("s15_music.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s15_music.mp3", 9, 40, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  2:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s16_window_vocals.mp3;s16_vocals.mp3", [25, 20, 50], 1, 0, 0)
                        audioEvent.register("s16_fireplace_vocals.mp3", 1, 25, 1, 0, 0)
                        audioEvent.register("s16_clock_vocals.mp3", 0, 25, 1, 0, 1)
                        audioEvent.register("s16_music.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s16_music.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s16_music.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s16_music.mp3", 3, 20, 1, 0, 1)
                        audioEvent.register("s16_music.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s16_music.mp3", 9, 40, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  2:
                    if dateArray[4] == 20:
                        audioEvent = audio.event()
                        audioEvent.register("s17.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s17.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s17.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s17.mp3", 3, 15, 1, 0, 1)
                        audioEvent.register("s17.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s17.mp3", 9, 35, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  2:
                    if dateArray[4] == 40:
                        audioEvent = audio.event()
                        audioEvent.register("s18.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s18.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s18.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s18.mp3", 3, 15, 1, 0, 1)
                        audioEvent.register("s18.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s18.mp3", 9, 35, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  3:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.register("s19.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s19.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s19.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s19.mp3", 3, 15, 1, 0, 1)
                        audioEvent.register("s19.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s19.mp3", 9, 35, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  3:
                    if dateArray[4] == 25:
                        audioEvent = audio.event()
                        audioEvent.register("s20.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s20.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s20.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s20.mp3", 3, 15, 1, 0, 1)
                        audioEvent.register("s20.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s20.mp3", 9, 35, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  3:
                    if dateArray[4] == 45:
                        audioEvent = audio.event()
                        audioEvent.register("s21.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s21.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s21.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s21.mp3", 3, 15, 1, 0, 1)
                        audioEvent.register("s21.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s21.mp3", 9, 35, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  4:
                    if dateArray[4] == 0:
                        audioEvent = audio.event()
                        audioEvent.register("s22.mp3", 0, 20, 1, 0, 1)
                        audioEvent.register("s22.mp3", 1, 20, 1, 0, 1)
                        audioEvent.register("s22.mp3", 2, 20, 1, 0, 1)
                        audioEvent.register("s22.mp3", 3, 15, 1, 0, 1)
                        audioEvent.register("s22.mp3", 7, 20, 1, 0, 1)
                        audioEvent.register("s22.mp3", 9, 35, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
                if dateArray[3] ==  9:
                    if dateArray[4] == 30 :
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s23_window_vocals.mp3;s23_vocals.mp3", [100, 25, 70], 1, 0, 0)
                        audioEvent.register("s23_fireplace_vocals.mp3", 1, 100, 1, 0, 0)
                        audioEvent.register("s23_clock_vocals.mp3", 0, 100, 1, 0, 1)
                        audioEvent.register("s23_music.mp3", 0, 70, 1, 0, 1)
                        audioEvent.register("s23_music.mp3", 1, 70, 1, 0, 1)
                        audioEvent.register("s23_music.mp3", 2, 70, 1, 0, 1)
                        audioEvent.register("s23_music.mp3", 3, 25, 1, 0, 1)
                        audioEvent.register("s23_music.mp3", 7, 70, 1, 0, 1)
                        audioEvent.register("s23_music.mp3", 9, 50, 1, 0, 1)
                        audioEvent.run()
                        time.sleep(60)
            elif (((dateArray[3] == 13) and (dateArray[4] == 6)) or ((dateArray[3] == 15) and (dateArray[4] == 6))or ((dateArray[3] == 17) and (dateArray[4] == 6))) or globals.doSchedualed:
                if dateArray[2] == 19:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci1.mp3", 6, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                if dateArray[2] == 20:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci2.mp3", 6, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                if dateArray[2] == 21:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci3.mp3", 9, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                if dateArray[2] == 22:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci4.mp3", 9, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                if dateArray[2] == 23:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci5.mp3", 12, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
