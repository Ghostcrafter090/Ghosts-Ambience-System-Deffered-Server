import modules.pytools as pytools
from PIL import Image
import modules.coord as coord

level = {
    -1: [False, [0, 0]]
}

class image:
    def getRgbAtPixel(levelNumber, x, y):
        return level[levelNumber][0][x, y]
    
def loadLevel(number: int):
    level[number] = [[], []]
    level[number][0] = Image.open("floorplan_" + str(number) + ".png").load()
    x = 0
    y = 0
    f = True
    while f:
        try:
            level[number][0][x, 0]
        except:
            f = False
        x = x + 1
    f = True
    while f:
        try:
            level[number][0][0, y]
        except:
            f = False
        y = y + 1
    level[number][1] = [x, y]

class map:
    def rotSearch(levelNumber, x, y, r):
        try:
            rgb = image.getRgbAtPixel(int(levelNumber), x, y)
        except:
            rgb = (0, 0, 0)
        n = 0
        f = True
        xf = x
        yf = y
        while (rgb[2] < 240) and f:
            vector = coord.dialation.get(n, r)
            xf = x + (vector[0] * n)
            yf = y + (vector[1] * n)
            try:
                rgb = image.getRgbAtPixel(int(levelNumber), xf, yf)
            except:
                f = False
            n = n + 1
        return [xf, yf]
    
    def getRot(c, d, x, y):
        a = x - c
        b = y - d
        while ((a > 1) or (a < -1)) or ((b > 1) or (b < -1)):
            rrand = 1
            a = a / 2
            b = b / 2
        return [a, b]
    
    def getMuffle(levelNumber, x, y, a, b):
        vector = map.getRot(x, y, a, b)
        try:
            rgb = image.getRgbAtPixel(int(levelNumber), x, y)
        except:
            rgb = (0, 0, 0)
        n = 0
        xf = x
        yf = y
        xfv = x
        yfv = y
        f = True
        muffle = 0
        while ((((a - 5) < xfv < (a + 5)) and ((b - 5) < yfv < (b + 5))) == False) and (f):
            xfv = xf + (vector[0] * n)
            yfv = yf + (vector[1] * n)
            try:
                rgb = image.getRgbAtPixel(int(levelNumber), xfv, yfv)
                if (rgb[2] > 100):
                    muffle = muffle + 5
                else:
                    muffle = muffle + 0.01
            except:
                f = False
            n = n + 1
            
        return muffle

    def vectorSearch(levelNumber, x, y, vector):
        try:
            rgb = image.getRgbAtPixel(int(levelNumber), x, y)
        except:
            rgb = (0, 0, 0)
        n = 0
        xf = x
        yf = y
        f = True
        while (rgb[2] < 100) and (f):
            xf = xf + (vector[0] * n)
            yf = yf + (vector[1] * n)
            try:
                rgb = image.getRgbAtPixel(int(levelNumber), xf, yf)
            except:
                f = False
            n = n + 1
            
        return [xf, yf]
    
    
    
    