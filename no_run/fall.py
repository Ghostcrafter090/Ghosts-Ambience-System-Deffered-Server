import modules.audio as audio
import modules.pytools as pytools
import time
import math
import api.wind
import modules.logManager as log
import random
import copy

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "volume": {
            "early": 0,
            "mid": 0,
            "late": 0,
            "end": 0
        },
        "volume_random": {
            "early": 0,
            "mid": 0,
            "late": 0,
            "end": 0
        },
        "dryness": 0
    }
    
audioBuffer = audio.rapidFire(60)
    
class tools:
    def getDayMin(dateArray):
        return (dateArray[3] * 60) + (dateArray[4])
    
    augustHumidityAverage = {1: 75.8, 2: 74.38571428571427, 3: 73.72857142857143, 4: 76.21428571428571, 5: 85.07142857142857, 6: 76.6, 7: 72.79999999999998, 8: 73.95714285714284, 9: 84.08571428571427, 10: 83.88571428571429, 11: 80.5142857142857, 12: 76.78571428571429, 13: 81.08571428571429, 14: 80.85714285714286, 15: 81.38571428571429, 16: 78.04285714285716, 17: 74.77142857142857, 18: 86.42857142857143, 19: 83.8, 20: 77.55714285714285, 21: 80.05714285714285, 22: 80.55714285714286, 23: 77.88571428571429, 24: 77.7, 25: 80.75714285714285, 26: 79.42857142857143, 27: 79.78571428571429, 28: 73.54285714285716, 29: 74.9, 30: 85.38571428571429, 31: 79.85714285714286}
    septemberHumidityAverage = {1: 76.85714285714286, 2: 78.05714285714285, 3: 81.17142857142858, 4: 80.97142857142856, 5: 74.5142857142857, 6: 77.14285714285714, 7: 82.74285714285715, 8: 80.27142857142857, 9: 79.88571428571429, 10: 81.31428571428572, 11: 84.2, 12: 83.92857142857143, 13: 80.44285714285715, 14: 81.25714285714285, 15: 76.81428571428572, 16: 79.25714285714285, 17: 78.17142857142856, 18: 79.60000000000001, 19: 79.04285714285713, 20: 78.27142857142857, 21: 78.65714285714286, 22: 81.85714285714286, 23: 82.3, 24: 81.52857142857142, 25: 77.57142857142857, 26: 86.89999999999999, 27: 88.22857142857143, 28: 87.12857142857145, 29: 86.58571428571429, 30: 80.21428571428571}
    
class util:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

def main():
    
    try:
        dryness = pytools.IO.getJson("dryness.json")["value"]
    except:
        dryness = 0
        
    while not status.exit:
        try:
            dataArray = util.dataGrabber()
        except:
            dataArray = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        dateArray = pytools.clock.getDateTime()
        
        if dataArray[0][4] == "rain":
            dryness = dryness - 10864.0
        if dataArray[0][4] == "lightrain":
            dryness = dryness - 5432.0
        if dataArray[0][4] == "mist":
            dryness = dryness - 2716.0
        if dataArray[0][4] == "thunder":
            dryness = dryness - 16296.0
        if dataArray[0][4] == "snow":
            dryness = dryness - 10864.0
        
        dryness = dryness + (194 * ((0.342567 ** (0.033542 * dataArray[0][8] - 10.51175) - 2138.34331) / (3600)))
        
        if dryness < 0:
            dryness = 0
        
        pytools.IO.saveJson("dryness.json", {
            "value": dryness
        })
        
        if (dateArray[1] < 12) and (dateArray[1] > 6):
            if dateArray[1] > 8:
                volume = -10
                if ((dateArray[1] == 9) and (dateArray[2] >= 15)) or ((dateArray[1] == 10) and (dateArray[2] <= 15)):
                    if dateArray[1] == 9:
                        volume = 100 * (math.fabs(1440 / (((30 * 24 * 60) - ((dateArray[2] * 24 * 60) + tools.getDayMin(dateArray))) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                    else:
                        volume = 100 * (math.fabs(1440 / ((((dateArray[2] - 1) * 24 * 60) + tools.getDayMin(dateArray)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                    
                    if volume > 75:
                        volume = 75
                        
                    status.vars["volume"]["early"] = volume
                    audioBuffer.playSoundWindow("leaves_early_m.mp3;leaves_early.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
                elif (dateArray[1] == 9) and (dateArray[2] < 15):
                    volume = (((1296000 - (pytools.clock.dateArrayToUTC([dateArray[0], 9, 15, 0, 0, 0]) - pytools.clock.dateArrayToUTC(dateArray))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                    
                    if volume > 0:
                        if volume > 75:
                            volume = 75
                            
                        status.vars["volume"]["early"] = volume
                        audioBuffer.playSoundWindow("leaves_early_m.mp3;leaves_early.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
                else:
                    volume = (((1296000 - (pytools.clock.dateArrayToUTC(dateArray) - pytools.clock.dateArrayToUTC([dateArray[0], 10, 15, 0, 0, 0]))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                    if volume > 0:
                        if volume > 75:
                            volume = 75
                        status.vars["volume"]["early"] = volume
                        audioBuffer.playSoundWindow("leaves_early_m.mp3;leaves_early.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            
            volume = -10
            if (dateArray[1] == 10) and (dateArray[2] < 25):
                if dateArray[2] <= 12:
                    volume = 100 * (math.fabs(1440 / (((12 * 24 * 60) - ((dateArray[2] * 24 * 60) + tools.getDayMin(dateArray))) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((((dateArray[2] - 1) * 24 * 60) - (12 * 24 * 60) + tools.getDayMin(dateArray)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                
                if volume > 75:
                    volume = 75
                status.vars["volume"]["mid"] = volume
                audioBuffer.playSoundWindow("leaves_mid_m.mp3;leaves_mid.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif (dateArray[1] == 9):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC([dateArray[0], 10, 1, 0, 0, 0]) - pytools.clock.dateArrayToUTC(dateArray))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    
                    status.vars["volume"]["mid"] = volume
                    audioBuffer.playSoundWindow("leaves_mid_m.mp3;leaves_mid.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif (dateArray[1] >= 10):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC(dateArray) - pytools.clock.dateArrayToUTC([dateArray[0], 10, 25, 0, 0, 0]))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume"]["mid"] = volume
                    audioBuffer.playSoundWindow("leaves_mid_m.mp3;leaves_mid.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            
            dateArray15Days = copy.deepcopy(dateArray)
            dateArray15Days[2] = dateArray15Days[2] + 15
            if dateArray15Days[2] > pytools.clock.getMonthEnd(dateArray15Days[1]):
                dateArray15Days[2] = dateArray15Days[2] - pytools.clock.getMonthEnd(dateArray15Days[1])
                dateArray15Days[1] = dateArray15Days[1] + 1
            
            if (dateArray15Days[1] == 10) and (dateArray15Days[2] < 25):
                if dateArray15Days[2] <= 12:
                    volume = 100 * (math.fabs(1440 / (((12 * 24 * 60) - ((dateArray15Days[2] * 24 * 60) + tools.getDayMin(dateArray15Days))) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((((dateArray15Days[2] - 1) * 24 * 60) - (12 * 24 * 60) + tools.getDayMin(dateArray15Days)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 75:
                    volume = 75
                status.vars["volume_random"]["mid"] = volume
                # audioBuffer.playSoundWindow("leaves_mid_m.mp3;leaves_mid.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif (dateArray15Days[1] == 9):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC([dateArray15Days[0], 10, 1, 0, 0, 0]) - pytools.clock.dateArrayToUTC(dateArray15Days))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume_random"]["mid"] = volume
                    # audioBuffer.playSoundWindow("leaves_mid_m.mp3;leaves_mid.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif (dateArray15Days[1] >= 10):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC(dateArray15Days) - pytools.clock.dateArrayToUTC([dateArray15Days[0], 10, 25, 0, 0, 0]))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume_random"]["mid"] = volume
                    # audioBuffer.playSoundWindow("leaves_mid_m.mp3;leaves_mid.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            
            if (300 * random.random()) < volume:
                randomVolumeModif = random.random()
                audioBuffer.playSoundWindow("leaves_mid_m.mp3;leaves_mid.mp3", [volume * randomVolumeModif, volume * 1.2 * randomVolumeModif, (volume / 4.5) * randomVolumeModif], 1.0, 0.0, 0)
            
            volume = -10
            if (dateArray[1] == 10) and ((dateArray[2] >= 10) and (dateArray[2] <= 30)):
                if dateArray[2] <= 20:
                    volume = 100 * (math.fabs(1440 / (((20 * 24 * 60) - (dateArray[2] * 24 * 60) + tools.getDayMin(dateArray)) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((dateArray[2] * 24 * 60) - (20 * 24 * 60) + tools.getDayMin(dateArray))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                
                if (6 < dateArray[1] < 11):
                    if dryness > 950400:
                        volume = volume + ((dryness - 950400) / 3600)
                
                if volume > 75:
                    volume = 75
                status.vars["volume"]["late"] = volume
                audioBuffer.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif ((dateArray[1] == 10) and (dateArray[2] < 10)) or (dateArray[1] == 9):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC([dateArray[0], 10, 10, 0, 0, 0]) - pytools.clock.dateArrayToUTC(dateArray))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                
                if (6 < dateArray[1] < 11):
                    if dryness > 950400:
                        volume = volume + ((dryness - 950400) / 3600)
                
                if volume > 0:
                    
                    if volume > 75:
                        volume = 75
                    status.vars["volume"]["late"] = volume
                    audioBuffer.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif ((dateArray[1] == 10) and (dateArray[2] > 30)) or (dateArray[1] == 11):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC(dateArray) - pytools.clock.dateArrayToUTC([dateArray[0], 10, 30, 0, 0, 0]))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                
                if (6 < dateArray[1] < 11):
                    if dryness > 950400:
                        volume = volume + ((dryness - 950400) / 3600)
                
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume"]["late"] = volume
                    audioBuffer.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            
            elif dryness > 950400:
                if (6 < dateArray[1] < 11):
                    volume = ((dryness - 950400) / 3600) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                    
                    if volume > 75:
                        volume = 75
                        
                    status.vars["volume"]["late"] = volume
                    audioBuffer.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume * random.random(), volume * 1.2 * random.random(), (volume / 4.5) * random.random()], 1.0, 0.0, 0)
            
            dateArray15Days = copy.deepcopy(dateArray)
            dateArray15Days[2] = dateArray15Days[2] + 15
            if dateArray15Days[2] > pytools.clock.getMonthEnd(dateArray15Days[1]):
                dateArray15Days[2] = dateArray15Days[2] - pytools.clock.getMonthEnd(dateArray15Days[1])
                dateArray15Days[1] = dateArray15Days[1] + 1
            
            if (dateArray15Days[1] == 10) and ((dateArray15Days[2] >= 10) and (dateArray15Days[2] <= 30)):
                if dateArray15Days[2] <= 20:
                    volume = 100 * (math.fabs(1440 / (((20 * 24 * 60) - (dateArray15Days[2] * 24 * 60) + tools.getDayMin(dateArray15Days)) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((dateArray15Days[2] * 24 * 60) - (20 * 24 * 60) + tools.getDayMin(dateArray15Days))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                
                if (6 < dateArray[1] < 11):
                    if dryness > 950400:
                        volume = volume + ((dryness - 950400) / 3600)
                
                if volume > 75:
                    volume = 75
                status.vars["volume_random"]["late"] = volume
                # audioBuffer.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif ((dateArray15Days[1] == 10) and (dateArray15Days[2] < 10)) or (dateArray15Days[1] == 9):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC([dateArray15Days[0], 10, 10, 0, 0, 0]) - pytools.clock.dateArrayToUTC(dateArray15Days))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                
                if (6 < dateArray[1] < 11):
                    if dryness > 950400:
                        volume = volume + ((dryness - 950400) / 3600)
                
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume_random"]["late"] = volume
                    # audioBuffer.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif ((dateArray15Days[1] == 10) and (dateArray15Days[2] > 30)) or (dateArray15Days[1] == 11):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC(dateArray15Days) - pytools.clock.dateArrayToUTC([dateArray15Days[0], 10, 30, 0, 0, 0]))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                
                if (6 < dateArray[1] < 11):
                    if dryness > 950400:
                        volume = volume + ((dryness - 950400) / 3600)
                
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume_random"]["late"] = volume
                    # audioBuffer.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            
            if (300 * random.random()) < volume:
                randomVolumeModif = random.random()
                audioBuffer.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume * randomVolumeModif, volume * 1.2 * randomVolumeModif, (volume / 4.5) * randomVolumeModif], 1.0, 0.0, 0)
            
            volume = -10
            if ((dateArray[1] == 10) and (dateArray[2] >= 20)) or ((dateArray[1] == 11) and (dateArray[2] <= 5)):
                if dateArray[1] == 10:
                    if dateArray[2] <= 28:
                        volume = 100 * (math.fabs(1440 / ((28 * 24 * 60) - (dateArray[2] * 24 * 60) + tools.getDayMin(dateArray) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                    else:
                        volume = 100 * (math.fabs(1440 / ((((dateArray[2] - 1) * 24 * 60) - (28 * 24 * 60) + tools.getDayMin(dateArray)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((((dateArray[1] - 1) * 24 * 60) + (3 * 24 * 60) + tools.getDayMin(dateArray)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 75:
                    volume = 75
                status.vars["volume"]["end"] = volume
                audioBuffer.playSoundWindow("leaves_end_m.mp3;leaves_end.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif (dateArray[1] == 10) and (dateArray[2] < 20):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC([dateArray[0], 10, 20, 0, 0, 0]) - pytools.clock.dateArrayToUTC(dateArray))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume"]["end"] = volume
                    audioBuffer.playSoundWindow("leaves_end_m.mp3;leaves_end.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif (dateArray[1] == 11):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC(dateArray) - pytools.clock.dateArrayToUTC([dateArray[0], 11, 5, 0, 0, 0]))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume"]["end"] = volume
                    audioBuffer.playSoundWindow("leaves_end_m.mp3;leaves_end.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
                    
            dateArray15Days = copy.deepcopy(dateArray)
            dateArray15Days[2] = dateArray15Days[2] + 15
            if dateArray15Days[2] > pytools.clock.getMonthEnd(dateArray15Days[1]):
                dateArray15Days[2] = dateArray15Days[2] - pytools.clock.getMonthEnd(dateArray15Days[1])
                dateArray15Days[1] = dateArray15Days[1] + 1
            
            if ((dateArray15Days[1] == 10) and (dateArray15Days[2] >= 20)) or ((dateArray15Days[1] == 11) and (dateArray15Days[2] <= 5)):
                if dateArray15Days[1] == 10:
                    if dateArray15Days[2] <= 28:
                        volume = 100 * (math.fabs(1440 / ((28 * 24 * 60) - (dateArray15Days[2] * 24 * 60) + tools.getDayMin(dateArray15Days) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                    else:
                        volume = 100 * (math.fabs(1440 / ((((dateArray15Days[2] - 1) * 24 * 60) - (28 * 24 * 60) + tools.getDayMin(dateArray15Days)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((((dateArray15Days[1] - 1) * 24 * 60) + (3 * 24 * 60) + tools.getDayMin(dateArray15Days)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 75:
                    volume = 75
                status.vars["volume_random"]["end"] = volume
                # audioBuffer.playSoundWindow("leaves_end_m.mp3;leaves_end.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif (dateArray15Days[1] == 10) and (dateArray15Days[2] < 20):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC([dateArray15Days[0], 10, 20, 0, 0, 0]) - pytools.clock.dateArrayToUTC(dateArray15Days))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume_random"]["end"] = volume
                    # audioBuffer.playSoundWindow("leaves_end_m.mp3;leaves_end.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            elif (dateArray15Days[1] == 11):
                volume = (((1296000 - (pytools.clock.dateArrayToUTC(dateArray15Days) - pytools.clock.dateArrayToUTC([dateArray15Days[0], 11, 5, 0, 0, 0]))) / 1296000) * 25.819291312853025) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                if volume > 0:
                    if volume > 75:
                        volume = 75
                    status.vars["volume_random"]["end"] = volume
                    # audioBuffer.playSoundWindow("leaves_end_m.mp3;leaves_end.mp3", [volume, volume * 1.2, volume / 4.5], 1.0, 0.0, 0)
            
            if (300 * random.random()) < volume:
                randomVolumeModif = random.random()
                audioBuffer.playSoundWindow("leaves_end_m.mp3;leaves_end.mp3", [volume * randomVolumeModif, volume * 1.2 * randomVolumeModif, (volume / 4.5) * randomVolumeModif], 1.0, 0.0, 0)
                    
            time.sleep(250)
        else:
            time.sleep(600)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    audioBuffer._start()
    main()
    audioBuffer._stop()
    status.hasExited = True
