import modules.pytools as pytools
import os

def getSnapshot():
    os.system("austin -p " + str(pytools.IO.getFile(".\\ambience_pid.cx")) + " -o test.flame -x 1")
    return pytools.IO.getFile("test.flame")

def getNumberOfThreads(flameData):
    
    threadIds = []
    
    for line in flameData.split("\n"):
        try:
            if line[0] == "P":
                if line.split(";")[1] not in threadIds:
                    threadIds.append(line.split(";")[1])
        except:
            pass
                
    return len(threadIds)
    