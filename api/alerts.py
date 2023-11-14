import modules.audio as audio
import modules.pytools as pytools
import gtts
import time
import traceback
from bs4 import BeautifulSoup as bs
import modules.logManager as log

print = log.printLog

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
        
        if (globals.textsf == [""]) or (globals.textsf == ["Warning! The alert system has encountered an error. Please contact Ghost Spectora at phantombrospb@gmail.com for more information."]):
            try:
                globals.textsf = pytools.IO.getJson(".\\alertData.json")["lastAlert"]
            except:
                globals.textsf = ["Warning! The alert system has encountered an error. Please contact Ghost Spectora at phantombrospb@gmail.com for more information."]
        
        dateArray = pytools.clock.getDateTime()
        try:
            dayTimes = pytools.IO.getList("dayTimes.pyl")[1]
        except:
            dayTimes = [[2022, 10, 21, 6, 0, 22], [2022, 10, 21, 6, 34, 14], [2022, 10, 21, 7, 8, 19], [2022, 10, 21, 7, 36, 33], [2022, 10, 21, 12, 59, 1], [2022, 10, 21, 18, 21, 28], [2022, 10, 21, 18, 49, 43], [2022, 10, 21, 19, 23, 47], [2022, 10, 21, 19, 57, 39]]
        try:
            texts = pytools.net.getTextAPI("https://www.weather.gc.ca/warnings/report_e.html?ns16").split(" Access city")[1].split("Weather shortcuts")[0].split("\n")
            textHTML = pytools.net.getRawAPI("https://www.weather.gc.ca/warnings/report_e.html?ns16=", False)
            soup = bs(textHTML, 'html.parser')
            # soup.attrs("innerText")
            mainContent = soup.find_all("main")[0].find_all("section")[0]
            texts = mainContent.get_text(separator="\n").replace("Pictou County\n Pictou County", "Pictou County\n").split('\n')
        except:
            print(traceback.format_exc())
            texts = globals.textsf
        
        print(texts)
        
        pytools.IO.saveJson(".\\alertData.json", {
            "lastAlert": texts
        })
        
        out = True
        french = False
        for n in texts:
            if n.lower().find("no alerts in effect") != -1:
                out = False
            if n.lower().find("the web address you have entered is incorrect") != -1:
                out = False
                french = True
            if n.lower().find("aucune alerte en vigueur") != -1:
                out = False
                french = True
        
        f = 0
             
        if not out:
            if not french:
                if len(globals.textsf) == len(texts):
                    i = 0
                    f = 0
                    for n in globals.textsf:
                        try:
                            if n != texts[i]:
                                f = f + 1
                        except:
                            f = f + 1
                        i = i + 1
                else:
                    f = 2
        if f > 1:
            out = True
            
        if globals.textsf == ["Warning! The alert system has encountered an error. Please contact Ghost Spectora at phantombrospb@gmail.com for more information."]:
            texts = globals.textsf
            out = True
            f = 2
        
        if out:
            if f < 2:
                if len(globals.textsf) == len(texts):
                    i = 0
                    f = 0
                    for n in globals.textsf:
                        try:
                            if n != texts[i]:
                                f = f + 1
                        except:
                            f = f + 1
                        i = i + 1
                else:
                    f = 2
            if f > 1:
                audioEvent = audio.event()
                if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                    audioEvent.register("alert_incoming.mp3", 2, 25, 1.0, 0.0, 1)
                else:
                    audioEvent.register("alert_incoming_night.mp3", 2, 10, 1.0, 0.0, 1)
                audioEvent.run(sendFile=True)
                nf = 0
                for n in texts:
                    try:
                        if n != ' ':
                            nf = nf + 1
                            print("Speaking: " + n)
                            gtts.gTTS(text=n, lang="en", slow=False).save(".\\sound\\assets\\alerts_" + str(nf) + ".mp3")
                            audioEvent = audio.event()
                            if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                                audioEvent.register("alerts_" + str(nf) + ".mp3", 2, 25, 1.0, 0.0, 1)
                            else:
                                audioEvent.register("alerts_" + str(nf) + ".mp3", 2, 15, 1.0, 0.0, 1,)
                            audioEvent.run(sendFile=True)
                    except:
                        print(traceback.format_exc())
                audioEvent = audio.event()
                if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                    audioEvent.register("alert_end.mp3", 2, 25, 1.0, 0.0, 1)
                else:
                    audioEvent.register("alert_end_night.mp3", 2, 10, 1.0, 0.0, 1)
                audioEvent.run(sendFile=True)
                globals.textsf = texts
            if (dateArray[3] % 6) == 0:
                if (dateArray[4] % 60) == 0:
                    audioEvent = audio.event()
                    if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                        audioEvent.register("alert_reproduce.mp3", 2, 25, 1.0, 0.0, 1)
                    else:
                        audioEvent.register("alert_reproduce_night.mp3", 2, 10, 1.0, 0.0, 1)
                    audioEvent.run(sendFile=True)
                    for n in texts:
                        try:
                            if n != ' ':
                                nf = nf + 1
                                gtts.gTTS(text=n, lang="en", slow=False).save(".\\sound\\assets\\alerts_" + str(nf) + ".mp3")
                                audioEvent = audio.event()
                                if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                                    audioEvent.register("alerts_" + str(nf) + ".mp3", 2, 25, 1.0, 0.0, 1)
                                else:
                                    audioEvent.register("alerts_" + str(nf) + ".mp3", 2, 15, 1.0, 0.0, 1)
                                audioEvent.run(sendFile=True)
                        except:
                            pass
                    audioEvent = audio.event()
                    if (pytools.clock.dateArrayToUTC(dayTimes[3]) < pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5])):
                        audioEvent.register("alert_end.mp3", 2, 25, 1.0, 0.0, 1)
                    else:
                        audioEvent.register("alert_end_night.mp3", 2, 10, 1.0, 0.0, 1)
                    audioEvent.run(sendFile=True)
        time.sleep(10)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
    
def run():
    status.hasExited = False
    main()
    status.hasExited = True
