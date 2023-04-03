import modules.audio as audio
import modules.pytools as pytools
import gtts
import time
import traceback

class status:
    apiKey = ""
    audioObj = False
    finishedLoop = False
    exit = False
    hasExited = False
    vars = {
        "lastLoop": []
    }

class globals:
    textsf = [""]

def main():
    while not status.exit:
        dateArray = pytools.clock.getDateTime()
        try:
            dayTimes = pytools.IO.getList("dayTimes.pyl")[1]
        except:
            dayTimes = [[2022, 10, 21, 6, 0, 22], [2022, 10, 21, 6, 34, 14], [2022, 10, 21, 7, 8, 19], [2022, 10, 21, 7, 36, 33], [2022, 10, 21, 12, 59, 1], [2022, 10, 21, 18, 21, 28], [2022, 10, 21, 18, 49, 43], [2022, 10, 21, 19, 23, 47], [2022, 10, 21, 19, 57, 39]]
        try:
            texts = pytools.net.getTextAPI("https://www.weather.gc.ca/warnings/report_e.html?ns16").split(" Access city")[1].split("Weather shortcuts")[0].split("\n")
        except:
            texts = globals.textsf
        out = True
        for n in texts:
            if n.find("No Alerts in effect") != -1:
                out = False
        if out:
            if globals.textsf != texts:
                if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                    audio.playSoundWindow("alert_incoming.mp3;alert_incoming.mp3", 25, 1.0, 0.0, 1)
                else:
                    audio.playSoundWindow("alert_incoming_night.mp3;alert_incoming_night.mp3", 10, 1.0, 0.0, 1)
                nf = 0
                for n in texts:
                    try:
                        if n != ' ':
                            nf = nf + 1
                            gtts.gTTS(text=n, lang="en", slow=False).save(".\\sound\\assets\\alerts_" + str(nf) + ".mp3")
                            if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                                audio.playSoundWindow("alerts_" + str(nf) + ".mp3;alerts_" + str(nf) + ".mp3", 25, 1.0, 0.0, 1, sendFile=True)
                            else:
                                audio.playSoundWindow("alerts_" + str(nf) + ".mp3;alerts_" + str(nf) + ".mp3", 15, 1.0, 0.0, 1, sendFile=True)
                    except:
                        print(traceback.format_exc())
                if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                    audio.playSoundWindow("alert_end.mp3;alert_end.mp3", 25, 1.0, 0.0, 1)
                else:
                    audio.playSoundWindow("alert_end_night.mp3;alert_end_night.mp3", 10, 1.0, 0.0, 1)
                globals.textsf = texts
            if (dateArray[3] % 6) == 0:
                if (dateArray[4] % 60) == 0:
                    if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                        audio.playSoundWindow("alert_reproduce.mp3;alert_reproduce.mp3", 25, 1.0, 0.0, 1)
                    else:
                        audio.playSoundWindow("alert_reproduce_night.mp3;alert_reproduce_night.mp3", 10, 1.0, 0.0, 1)
                    for n in texts:
                        try:
                            if n != ' ':
                                nf = nf + 1
                                gtts.gTTS(text=n, lang="en", slow=False).save(".\\sound\\assets\\alerts_" + str(nf) + ".mp3")
                                if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                                    audio.playSoundWindow("alerts_" + str(nf) + ".mp3;alerts_" + str(nf) + ".mp3", 25, 1.0, 0.0, 1, sendFile=True)
                                else:
                                    audio.playSoundWindow("alerts_" + str(nf) + ".mp3;alerts_" + str(nf) + ".mp3", 15, 1.0, 0.0, 1, sendFile=True)
                        except:
                            pass
                    if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                        audio.playSoundWindow("alert_end.mp3;alert_end.mp3", 25, 1.0, 0.0, 1)
                    else:
                        audio.playSoundWindow("alert_end_night.mp3;alert_end_night.mp3", 10, 1.0, 0.0, 1)
        time.sleep(10)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
    
def run():
    status.hasExited = False
    main()
    status.hasExited = True
