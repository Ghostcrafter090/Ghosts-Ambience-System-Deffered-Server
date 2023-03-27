import threading
import os
import subprocess
import time

class globals:
    main = False
    
class flags:
    pythonf = False
    remote = "localhost"

class tools:  
    def getRemote():
        if flags.remote == False:
            return "localhost"
        else:
            return flags.remote
        
    def inputOption(text: str, type):
        errork = True
        while errork:
            try:
                salt = type(input(text))
                errork = False
            except:
                print("Value incorrect. Please enter a value of type " + type.__name__ + ".")
        return salt

def runMain():
    """if flags.pythonf == False:
        if os.path.exists("C:\\windows\\py.exe"):
            flags.pythonf = "C:\\windows\\py.exe"
    if flags.pythonf == False:
        for n in os.environ["path"].split(";"): 
            if n.find("\\Python\\") != -1:
                flags.pythonf = n
    if flags.pythonf == False:
        flags.pythonf = input("Please specify the folder containing the python executable: ")
    if flags.pythonf[-4:] != ".exe":
        subprocess.getstatusoutput("copy \"" + flags.pythonf + "python.exe\" \".\\ambienceProfile.exe\" /y")[0]
        subprocess.getstatusoutput("copy \".\\ambienceProfile.exe\" \"" + flags.pythonf + "ambienceProfile.exe\" /y")[0]
    else:
        subprocess.getstatusoutput("copy \"" + flags.pythonf + "\" \".\\ambienceProfile.exe\" /y")[0]
        subprocess.getstatusoutput("copy \".\\ambienceProfile.exe\" \"" + flags.pythonf.replace("python.exe", "ambienceProfile.exe").replace("py.exe", "ambienceProfile.exe") + "\" /y")[0]
    """
    import main
    globals.main = main
    
def runAustin():
    print("cmd.exe /c austin -o \"Profiler.austin\" -Cfp " + str(os.getpid()))
    os.system("cmd.exe /c start /d \"..\\..\\austin_tui\" \"\" cmd.exe /k py10 __main__.py -C -p " + str(os.getpid()))
    os.system("cmd.exe /c austin -o \"Profiler.austin\" -Cfp " + str(os.getpid()))

threadMain = threading.Thread(target=runMain)
threadMain.start()

time.sleep(3)

threadAustin = threading.Thread(target=runAustin)
threadAustin.start()

threadMain.join()
threadAustin.join()
