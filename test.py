import modules.pytools as pytools
import sys
import os

import time

import threading

import modules.speed as speed
speed.run(doThreadCounter=False)

pl = False

class plugin:
    test = False
    
class globals:
    apiKey = ""

def debug(name, run=False):
    try:
        name = name.split("\\")[-1].split(".py")[0]
    except:
        pass
    global pl
    exec("""
import api.""" + name + """
plugin.test = api.""" + name + """
""")
    
    os.chdir(".\\working")
    
    plugin.test.status.apiKey = globals.apiKey

    if run:
        plugin.test.run()
    else:
        pl = plugin.test

runf = False
noPrint = False
if __name__ == "__main__":
    for n in sys.argv:
        if n.split("=") == "--apiKey":
            globals.apiKey = n.split("=")[1]
        if n == "--noPrint":
            noPrint = True
    try:
        if sys.argv[1] == "--run":
            if sys.argv[2]:
                runf = True
    except:
        print("Invalid syntax.")
        print("To test plugin: py testplugin.py --run <plugin_name>")

def printTic():
    while True:
        if not noPrint:
            print("GIL Timing Info: " + str((speed.vars.prevTic, sys.getswitchinterval())))
        time.sleep(1)
        
if runf:
    threading.Thread(target=printTic).start()
    debug(sys.argv[2], run=True)