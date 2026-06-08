import modules.pytools as pytools
import traceback

class globals:
    apiKey = False
    sectionName = False

def pollJavascriptFilename():
    try:
        if not globals.sectionName:
            raw = pytools.net.getRawAPI("https://openweathermap.org/", False)
            reference = str(raw).find("weather-app.")
            section = str(raw)[reference:reference + 40]
            globals.sectionName = section.split(".js")[0]
    except:
        print(traceback.format_exc())
        return False
    
    return globals.sectionName

def stealApiKey(name):
    try:
        if not globals.apiKey:
            javascript = pytools.net.getTextAPI("https://openweathermap.org/themes/openweathermap/assets/vendor/owm/js/" + name + ".js")
            reference = javascript.find("appid:")
            
            if len(javascript[reference:reference + 40].split(",")[0].split(":")[1].replace("\"", "")) > 10:
                globals.apiKey = javascript[reference:reference + 40].split(",")[0].split(":")[1].replace("\"", "")
    except:
        print(traceback.format_exc())
        return False
    
    return globals.apiKey

def getPublicApiKey():
    if not globals.apiKey:
        try:
            globals.apiKey = stealApiKey(pollJavascriptFilename())
        except:
            globals.apiKey = pytools.IO.getJson("access.key")["openweathermap"]
    
    return globals.apiKey