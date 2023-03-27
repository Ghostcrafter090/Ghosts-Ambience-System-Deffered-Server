# import modules.pytools as pytools
import time
import threading
import random
import hashlib

class benchmark:
    
    n = 0
    
    def add():
        if random.random() < 2:
            benchmark.n = benchmark.n + 1
    
    def get():
        listf = []
        
        while len(listf) < 100:
            startTic = round(time.time() * 1000000000)
            
            benchmark.n = 0
            while benchmark.n < 500:
                threading.Thread(target=benchmark.add).start()
                
            listf.append(1 / ((round(time.time() * 1000000000) - startTic) / 1000000000))
            
        return (sum(listf) / len(listf)) * 1000
    
    def getNumberOfPlugins(bench):
        a = 1.00008
        b = 1
        c = -28550.5
        d = -10.269
        
        return (a ** (b * (bench - c))) + d

class cipher:
    def hash(data):
        while len(data) > 1000:
            dataNew = b''
            n = 0
            while n < len(data):
                dataNew = dataNew + hashlib.md5(data[n:n + 100]).digest()
                n = n + 100
            data = dataNew
        return hashlib.md5(data).digest()