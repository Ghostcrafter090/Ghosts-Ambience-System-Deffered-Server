import modules.pytools as pytools
import os

def getSounds():
    sounds = []
    for file in os.listdir(".\\vars\\pluginSounds"):
        if os.path.exists(".\\vars\\pluginSounds\\" + file):
            raw = pytools.IO.getFile(".\\vars\\pluginSounds\\" + file)
            data = {
                "path": raw.split(";")[0],
                "channel": raw.split(";")[1],
                "event_start": float(raw.split(';')[2]),
            }
            if len(raw.split(";")) > 6:
                data["duration"] = float(raw.split(";")[3])
                data["volume"] = float(raw.split(";")[4])
                data["speed"] = float(raw.split(";")[5])
                data["wait"] = bool(raw.split(";")[6])
            else:
                data["duration"] = 0
                data["volume"] = float(raw.split(";")[3])
                data["speed"] = float(raw.split(";")[4])
                data["wait"] = bool(raw.split(";")[5])
            
            if (data["event_start"] + data["duration"]) >= pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                sounds.append(data)
        
    return sounds
    
def countSounds():
    soundData = getSounds()
    
    counts = {}
    
    for sound in soundData:
        if sound["path"] not in counts:
            counts[sound["path"]] = {
                "count": 0,
                "collectiveVolume": 0
            }
        counts[sound["path"]]["count"] = counts[sound["path"]]["count"] + 1
        counts[sound["path"]]["collectiveVolume"] = counts[sound["path"]]["collectiveVolume"] + sound["volume"]

    def _sortedKey(x):
        return counts[x]["count"]

    for count in sorted(counts, key=_sortedKey, reverse=True):
        print(count + "\t\t: " + str(counts[count]["count"]) + "\t\t(" + str(counts[count]["collectiveVolume"]) + ")")
        
        