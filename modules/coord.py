import math

class calc:
    def latKm(lat):
        return lat * 110.574
    
    def lonKm(lat, lon):
        return lon * math.cos(lat) * 111.320
    
    def kmLat(dist):
        return dist / 110.547
    
    def kmLon(dist, lat):
        return dist / (math.cos(lat) * 111.320)
    
    class trig:
        def sinx(opp, hyp):
            return math.sinh(opp / hyp)
        
        def coxx(adj, hyp):
            return math.cosh(adj / hyp)
        
        def tanx(opp, adj):
            return math.tanh(opp / adj)
        
        def getHyp(opp, adj):
            return ((opp ** 2) + (adj ** 2)) ** 0.5
        
        def getXy(angle):
            return [math.cos(angle), math.sin(angle)]

class dialation:
    def get(distance, angle):
        anglef = angle
        xY = calc.trig.getXy(anglef)
        return [xY[0] * distance, xY[1] * distance]
    
    def apply(lat, lon, n):
        latf = lat + calc.kmLat(n[0])
        lonf = lon + calc.kmLon(n[1], latf)
        return [latf, lonf]