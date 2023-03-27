import modules.audio as audio
import modules.pytools as pytools
import random
import time

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "locustChances": []
    }

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

    def dayTimesGrabber():
        dayTimes = pytools.IO.getList('daytimes.pyl')[1]
        if dayTimes == 1:
            dayTimes = [[2022, 5, 11, 3, 45, 15], [2022, 5, 11, 4, 34, 10], [2022, 5, 11, 5, 16, 33], [2022, 5, 11, 5, 48, 29], [2022, 5, 11, 13, 10, 47], [2022, 5, 11, 20, 33, 6], [2022, 5, 11, 21, 5, 2], [2022, 5, 11, 21, 47, 25], [2022, 5, 11, 22, 36, 20]]
        return dayTimes

class tools:
    def getDayOfYear(dateArray):
        dayOfYear = 0
        i = 1
        while i < dateArray[1]:
            dayOfYear = dayOfYear + pytools.clock.getMonthEnd(i)
            i = i + 1
        return dayOfYear + dateArray[2]

def main():
    while not status.exit:
        chance = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        dateArray = pytools.clock.getDateTime()
        dayOfYear = tools.getDayOfYear(dateArray)
        dataList = utils.dataGrabber()
        dayTimes = utils.dayTimesGrabber()

        try:
            num = dataList[0][7] - 15
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[0] = per / (((((300 - dayOfYear) ** 4) + 1) / 4100625) + 1)
        except:
            pass
        try:
            num = dataList[0][7] - 16
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[1] = per / (((((235 - dayOfYear) ** 4) + 1) / 4100625) + 1) / (101 - dataList[0][8])
        except:
            pass
        try:
            num = dataList[0][7] - 12
            if dataList[0][7] >= 19:
                num = num - ((dataList[0][7] - 18) * 2)
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[2] = per / (((((250 - dayOfYear) ** 4) + 1) / 4100625) + 1) / (101 - dataList[0][8])
        except:
            pass
        try:
            num = dataList[0][7] - 3
            if dataList[0][7] >= 20:
                num = num - ((dataList[0][7] - 19) * 2)
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[3] = per / (((((320 - dayOfYear) ** 4) + 1) / 4100625) + 1)
        except:
            pass
        try:
            num = dataList[0][7] - 15
            if dataList[0][7] >= 21:
                num = num - ((dataList[0][7] - 20) * 2)
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[4] = per / (((((240 - dayOfYear) ** 4) + 1) / 4100625) + 1)
        except:
            pass
        try:
            num = dataList[0][7] - 16 - (16 - dateArray[3])
            if dataList[0][7] >= 20:
                num = num - (dateArray[3] * 2)
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[5] = per / (((((230 - dayOfYear) ** 4) + 1) / 4100625) + 1)
        except:
            pass
        try:
            num = dataList[0][7] - 16 - (23 - dateArray[3])
            if dataList[0][7] <= 20:
                num = num - ((dataList[0][7] - 19) * 2)
            if dateArray[3] >= 6:
                num = num - (dateArray[3] * 2)
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[6] = per / (((((260 - dayOfYear) ** 4) + 1) / 4100625) + 1) / (101 - dataList[0][8])
        except:
            pass
        try:
            num = dataList[0][7] - 16 - (23 - dateArray[3])
            if dataList[0][7] <= 20:
                num = num - ((dataList[0][7] - 19) * 2)
            if dateArray[3] >= 18:
                num = num - (dateArray[3] * 2)
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[7] = per / ((((((260 - dayOfYear) ** 2) * ((280 - dayOfYear) ** 2)) + 1) / 4100625) + 1) / (50 - dataList[0][8])
        except:
            pass
        try:
            num = dataList[0][7] - 16 - (23 - dateArray[3])
            if dataList[0][7] <= 20:
                num = num - ((dataList[0][7] - 19) * 2)
            if dateArray[3] >= 6:
                num = num - (dateArray[3] * 2)
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[8] = per / (((((300 - dayOfYear) * ((260 - dayOfYear) ** 3)) + 1) / 4100625) + 1)
        except:
            pass
        try:
            num = dataList[0][7] - 8
            if dataList[0][7] <= 17:
                num = num - ((dataList[0][7] - 16) * 2)
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[9] = per / (((((190 - dayOfYear) ** 4) + 1) / 4100625) + 1)
        except:
            pass
        try:
            num = dataList[0][7] - 15
            if num < 0:
                num = 0
            per = (2 ** num) * 5
            chance[10] = per / (((((300 - dayOfYear) ** 4) + 1) / 4100625) + 1)
        except:
            pass

        speed = dataList[0][7] / 20
        if dataList[0][7] > 7:
            if (random.random() * 32768) < chance[5]:
                audio.playSoundWindow("slender_me_ka_m.mp3;slender_me_ka.mp3", 50, speed, 0, 0)
            if (random.random() * 32768) < chance[1]:
                audio.playSoundWindow("spahgnum_gr_cr_m.mp3;spahgnum_gr_cr.mp3", 50, speed, 0, 0)
            if (random.random() * 32768) < chance[2]:
                audio.playSoundWindow("striped_gr_cr_m.mp3;striped_gr_cr.mp3", 50, speed, 0, 0)
            if (random.random() * 32768) < chance[3]:
                audio.playSoundWindow("carolina_gr_cr_m.mp3;carolina_gr_cr.mp3", 50, speed, 0, 0)
            if (random.random() * 32768) < chance[4]:
                audio.playSoundWindow("allards_gr_cr_m.mp3;allards_gr_cr.mp3", 50, speed, 0, 0)
            
            if (random.random() * 32768) < chance[6]:
                if dateArray[3] >= dayTimes[1][3]:
                    if dateArray[3] <= dayTimes[7][3]:
                        audio.playSoundWindow("allards_gr_cr_m.mp3;allards_gr_cr.mp3", 50, speed, 0, 0)
            if (random.random() * 32768) < chance[6]:
                if dateArray[3] >= dayTimes[2][3]:
                    if dateArray[3] <= dayTimes[2][3]:
                        audio.playSoundWindow("allards_gr_cr_m.mp3;allards_gr_cr.mp3", 50, speed, 0, 0)
            
            if (random.random() * 32768) < chance[7]:
                audio.playSoundWindow("curvetail_bu_ka_m.mp3;curvetail_bu_ka.mp3", 50, speed, 0, 0)
            if (random.random() * 32768) < chance[8]:
                audio.playSoundWindow("forktail_bu_ka_m.mp3;forktail_bu_ka.mp3", 50, speed, 0, 0)
            if (random.random() * 32768) < chance[0]:
                audio.playSoundWindow("marsh_me_gr_m.mp3;marsh_me_gr.mp3", 50, speed, 0, 0)
            if (random.random() * 32768) < chance[9]:
                audio.playSoundWindow("says_ci_m.mp3;says_ci.mp3", 50, speed, 0, 0)
        else:
            time.sleep(60)
        
        if (random.random() * 32768) < chance[10]:
            if dateArray[3] < dayTimes[6][3]:
                if dateArray[3] >= dayTimes[2][3]:
                    audio.playSoundWindow("cicada_windowclosed.mp3;cicada_windowopen.mp3", 50, speed, 0, 0)
        status.vars['locustChances'] = chance
        try:
            time.sleep(30 / speed)
        except:
            time.sleep(60)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
