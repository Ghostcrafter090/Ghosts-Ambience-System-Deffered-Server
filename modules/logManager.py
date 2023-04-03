import modules.pytools as pytools

import os

def init():
    if os.path.exists(".\\working"):
        try:
            os.mkdir(".\\logs")
        except:
            pass
        try:
            os.mkdir(".\\logs\\system")
        except:
            pass
    else:
        try:
            os.mkdir("..\\logs")
        except:
            pass
        try:
            os.mkdir("..\\logs\\system")
        except:
            pass

def write(strf, pluginf="system"):
    
    if not os.path.exists("..\\logs\\system"):
        init()
    
    dateArray = pytools.clock.getDateTime()
    dateString = str(dateArray[0]) + "-" + str(dateArray[1]) + "-" + str(dateArray[2]) + "_" + str(dateArray[3]) + "."  + str(dateArray[4]) + "."  + str(dateArray[5])
    pytools.IO.appendFile(".\\logs\\system\\" + dateString + "_system.log", str(dateArray) + " ;;; " + pluginf + "; " + strf)
            
            
            