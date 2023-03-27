import modules.pytools as pytools
import PIL

def grabWindGusts():
    pictou = (155, 227)
    
    legend = [[(54, 0, 0), 23], [(92, 0, 0), 42], [(33, 0, 0), 47], [(168, 0, 1), 75], [(191, 1, 1), 90]]

    dateArray = pytools.clock.getDateTime()

    dateArray[3] = dateArray[3] + 4

    if dateArray[4] > 30:
        hour = dateArray[3] + 1
    else:
        hour = dateArray[3]

    if hour > 23:
        hour = hour - 23
        dateArray[2] = dateArray[2] + 1
        if dateArray[2] > pytools.clock.getMonthEnd(dateArray[1]):
            dateArray[2] = dateArray[2] - pytools.clock.getMonthEnd(dateArray[1])
            dateArray[1] == dateArray[1] + 1
            if dateArray[1] > 12:
                dateArray[1] = dateArray[1] - 12
                dateArray[0] = dateArray[0] + 1

    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)
        
    if dateArray[2] < 10:
        day = "0" + str(dateArray[2])
    else:
        day = str(dateArray[2])

    if dateArray[1] < 10:
        month = "0" + str(dateArray[1])
    else:
        month = str(dateArray[1])

    url = "https://ims.windy.com/im/v3.0/forecast/ecmwf-hres/" + str(dateArray[0]) + month + day + "00" + "/" + str(dateArray[0]) + month + day + hour + "/wm_grid_257/3/2/2/gust-surface.jpg"
    # url = "https://ims.windy.com/im/v3.0/forecast/ecmwf-hres/2023021400/2023021415/wm_grid_257/3/2/2/gust-surface.jpg"

    pytools.net.download(url, "windy_gusts.png", 1)

    imag = PIL.Image.open("windy_gusts.png")

    print(imag.getpixel(pictou))
    
