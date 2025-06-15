import modules.audio as audio
import modules.pytools as pytools
import time
import os
import modules.logManager as log
import random

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
    
class ambientTimes:
    outside = time.time()
    bookKeepers = time.time()

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

class utils:        
    def dayTimesGrabber():
        dayTimes = pytools.IO.getList('daytimes.pyl')[1]
        if dayTimes == 1:
            dayTimes = [[2022, 5, 11, 3, 45, 15], [2022, 5, 11, 4, 34, 10], [2022, 5, 11, 5, 16, 33], [2022, 5, 11, 5, 48, 29], [2022, 5, 11, 13, 10, 47], [2022, 5, 11, 20, 33, 6], [2022, 5, 11, 21, 5, 2], [2022, 5, 11, 21, 47, 25], [2022, 5, 11, 22, 36, 20]]
        return dayTimes

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
                        audio.playSoundAll("emccw1.mp3", 18, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 11:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw2.mp3", 36, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 12:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw3.mp3", 54, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 13:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw4.mp3", 72, 1, 0, 1)
                        time.sleep(60)
                if dateArray[3] == 14:
                    if dateArray[4] == 6:
                        audio.playSoundAll("emccw5.mp3", 90, 1, 0, 1)
                        time.sleep(60)
                        
                if ambientTimes.outside < time.time():
                    dayTimes = utils.dayTimesGrabber()
                    audioEvent = audio.event()
                    if pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5]):
                        audioEvent.registerWindow("emccs_window_day.mp3;emccs_outside_day.mp3", 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_day.mp3", 0, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_day.mp3", 1, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_day.mp3", 7, 100, 1.0, 0.0, 0)
                    elif (pytools.clock.dateArrayToUTC(dayTimes[5]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[7])) or (pytools.clock.dateArrayToUTC(dayTimes[1]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[3])):
                        audioEvent.registerWindow("emccs_window_day.mp3;emccs_outside_day.mp3", 100, 1.0, 0.0, 0)
                        audioEvent.registerWindow("emccs_window_night.mp3;emccs_outside_night.mp3", 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_day.mp3", 0, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_day.mp3", 1, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_day.mp3", 7, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_night.mp3", 0, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_night.mp3", 1, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_night.mp3", 7, 100, 1.0, 0.0, 0)
                    else:
                        audioEvent.registerWindow("emccs_window_night.mp3;emccs_outside_night.mp3", 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_night.mp3", 0, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_night.mp3", 1, 100, 1.0, 0.0, 0)
                        audioEvent.register("emccs_wall_night.mp3", 7, 100, 1.0, 0.0, 0)
                    audioEvent.run()
                    ambientTimes.outside = time.time() + 60
                
                if ambientTimes.bookKeepers < time.time():
                    dayTimes = utils.dayTimesGrabber()
                    audioEvent = audio.event()
                    if (dateArray[2] == 24) and (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC([dateArray[0], dateArray[1], dateArray[2], 18, 0, 0])):
                        audioEvent.register("book_keepers_clock.mp3", 0, 100, 1.0, 0.0, 0)
                        audioEvent.register("book_keepers_fireplace.mp3", 1, 100, 1.0, 0.0, 0)
                        audioEvent.register("book_keepers_generic.mp3", 7, 100, 1.0, 0.0, 0)
                    audioEvent.run()
                    ambientTimes.bookKeepers = time.time() + 60
                        
                if dateArray[3] == 15:
                    if dateArray[4] == 0:
                        audio.playSoundAll("s1_all.mp3", 100, 1, 0, 1)
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s2_window_vocals.mp3;s2_outside_vocals.mp3", [100, 85, 50], 1, 0, 0)
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
                        audioEvent.registerWindow("s3_window_vocals.mp3;s3_outside_vocals.mp3", [100, 85, 50], 1, 0, 0)
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
                        audioEvent.registerWindow("s4_window_vocals.mp3;s4_outside_vocals.mp3", [100, 85, 50], 1, 0, 0)
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
                        audioEvent.registerWindow("s5_window_vocals.mp3;s5_outside_vocals.mp3", [100, 60, 90], 1, 0, 0)
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
                        audioEvent.registerWindow("s6_window_vocals.mp3;s6_outside_vocals.mp3", [100, 50, 100], 1, 0, 0)
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
                        audioEvent.registerWindow("s8_window_vocals.mp3;s8_outside_vocals.mp3", [100, 85, 60], 1, 0, 0)
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
                        audioEvent.registerWindow("s9_window_vocals.mp3;s9_outside_vocals.mp3", [100, 80, 100], 1, 0, 0)
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
                if dateArray[3] == 19:
                    if dateArray[4] == 30:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s10_window_vocals.mp3;s10_outside_vocals.mp3", [100, 85, 50], 1, 0, 0)
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
                    
                if dateArray[3] == 22:
                    if dateArray[4] == 35:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s11_window_vocals.mp3;s11_outside_vocals.mp3", [100, 50, 60], 1, 0, 0)
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
                if dateArray[3] == 23:
                    if dateArray[4] == 30:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("s12_window_vocals.mp3;s12_outside_vocals.mp3", [100, 50, 50], 1, 0, 0)
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
                        audioEvent.registerWindow("s12.5_window_vocals.mp3;s12.5_vocals.mp3", [100, 70, 45], 1, 0, 0)
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
                        
                if (22 > dateArray[3] > 20) or ((dateArray[3] == 22) and (dateArray[4] < 33)):
                    if random.random() < 0.5:
                        audioEvent = audio.event()
                        audioEvent.register("scrooge_eating.mp3", 1, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                        audioEvent.run()
                        time.sleep(60)
                    else:
                        if (random.random() < (0.1 * (dateArray[4] / 35))) and (dateArray[3] == 22):
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("emccs_bell_" + str(random.randint(0, 5)) + ".mp3", randomSpeaker, random.randint(75, 100), 0.98 + (0.04 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(2)
                        elif (random.random() < (0.027777777777777776 * (dateArray[4] / 35))) and (dateArray[3] == 22):
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("draft_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(1, 20), 0.2 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(10)
                        elif (random.random() < (0.08333333333333333 * (dateArray[4] / 35))) and (dateArray[3] > 21):
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("h_chains_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(75, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(2)
                        elif random.random() < 0.1:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("g_creak_0.mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(5)
                        else:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("humbug_" + str(random.randint(0, 5)) + ".mp3", randomSpeaker, random.randint(25, 75), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(2)
                else: 
                    if ((18 < dateArray[3]) or ((18 == dateArray[3]) and (dateArray[4] > 20))) and ((dateArray[3] < 23) or ((dateArray[3] == 23) and (dateArray[4] < 30))):
                        if random.random() < 0.027777777777777776:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("scrooge_walking.mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(15)
                        elif (random.random() < 0.027777777777777776) and ((19 < dateArray[3]) or ((19 == dateArray[3]) and (dateArray[4] > 40))) and (dateArray[3] < 22):
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([2, 7])
                            audioEvent.register("scrooge_cooking.mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(15)
                        elif (random.random() < (0.027777777777777776 * (dateArray[4] / 35))) and (dateArray[3] == 22):
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("draft_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(1, 20), 0.2 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(10)
                        elif random.random() < 0.041666666666666664:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("g_door_" + str(random.randint(0, 7)) + ".mp3", randomSpeaker, random.randint(50, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(10)
                        elif random.random() < 0.041666666666666664:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("g_footsteps_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(5)
                        elif random.random() < 0.041666666666666664:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("g_creak_0.mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(5)
                        elif (random.random() < (0.08333333333333333 * (dateArray[4] / 35))) and (dateArray[3] > 21):
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("h_chains_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(75, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(2)
                        elif (random.random() < (0.1 * (dateArray[4] / 35))) and (dateArray[3] == 22):
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("emccs_bell_" + str(random.randint(0, 5)) + ".mp3", randomSpeaker, random.randint(75, 100), 0.98 + (0.04 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(2)
                        elif random.random() < 0.0833333333333333:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("humbug_" + str(random.randint(0, 5)) + ".mp3", randomSpeaker, random.randint(25, 75), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(2)
                    elif ((dateArray[3] == 23) and (dateArray[4] > 45)) or (dateArray[3] < 1) or ((dateArray[3] == 1) and (dateArray[4] > 15)) or ((dateArray[3] > 1) and (dateArray[3] < 9)):
                        if (random.random() < (0.08333333333333333 * (dateArray[4] / 35))):
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("h_chains_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(75, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(2)
                        elif random.random() < 0.041666666666666664:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("g_creak_0.mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(5)
                        elif random.random() < 0.041666666666666664:
                            audioEvent = audio.event()
                            randomSpeaker = random.choice([0, 1, 2, 7])
                            audioEvent.register("g_footsteps_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(5)
                        else:
                            audioEvent = audio.event()
                            audioEvent.register("scrooge_snoring.mp3", 1, random.randint(5, 50), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(60)
                    elif (dateArray[2] == 24) and (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC([dateArray[0], dateArray[1], dateArray[2], 18, 0, 0])):
                        if random.random() < 0.0233333333333333:
                            audioEvent = audio.event()
                            audioEvent.register("humbug_" + str(random.randint(0, 5)) + ".mp3", 1, random.randint(25, 75), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                            audioEvent.run()
                            time.sleep(2)
                    else:
                        if (dateArray[3] < 8) or (dateArray[3] > 21):
                            if (random.random() < (0.08333333333333333 * (dateArray[4] / 35))):
                                audioEvent = audio.event()
                                randomSpeaker = random.choice([0, 1, 2, 7])
                                audioEvent.register("h_chains_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(75, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                                audioEvent.run()
                                time.sleep(random.random() * 60)
                            elif random.random() < 0.041666666666666664:
                                audioEvent = audio.event()
                                randomSpeaker = random.choice([0, 1, 2, 7])
                                audioEvent.register("g_creak_0.mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                                audioEvent.run()
                                time.sleep(random.random() * 60)
                            elif random.random() < 0.041666666666666664:
                                audioEvent = audio.event()
                                randomSpeaker = random.choice([0, 1, 2, 7])
                                audioEvent.register("g_footsteps_" + str(random.randint(0, 2)) + ".mp3", randomSpeaker, random.randint(25, 100), 0.95 + (0.1 * random.random()), 0, 0, clock=False)
                                audioEvent.run()
                                time.sleep(random.random() * 60)
                            
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
                        audioEvent.registerWindow("s15_window_vocals.mp3;s15_vocals.mp3", [25, 50, 50], 1, 0, 0)
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
                        audioEvent.registerWindow("s16_window_vocals.mp3;s16_vocals.mp3", [25, 50, 50], 1, 0, 0)
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
                        audioEvent.registerWindow("s23_window_vocals.mp3;s23_vocals.mp3", [100, 60, 70], 1, 0, 0)
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
                        audio.playSoundAll("emcci1.mp3", 18, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                if dateArray[2] == 20:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci2.mp3", 36, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                if dateArray[2] == 21:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci3.mp3", 54, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                if dateArray[2] == 22:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci4.mp3", 72, 1, 0, 1)
                        time.sleep(60)
                        globals.doSchedualed = False
                    else:
                        globals.doSchedualed = True
                if dateArray[2] == 23:
                    if not os.path.exists("ch_music_playing.derp"):
                        audio.playSoundAll("emcci5.mp3", 90, 1, 0, 1)
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
