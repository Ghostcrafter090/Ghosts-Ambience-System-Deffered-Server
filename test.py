import modules.pytools as pytools
import sys
import os

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
if __name__ == "__main__":
    for n in sys.argv:
        if n.split("=") == "--apiKey":
            globals.apiKey = n.split("=")[1]
    try:
        if sys.argv[1] == "--run":
            if sys.argv[2]:
                runf = True
    except:
        print("Invalid syntax.")
        print("To test plugin: py testplugin.py --run <plugin_name>")
    
if runf:
    debug(sys.argv[2], run=True)