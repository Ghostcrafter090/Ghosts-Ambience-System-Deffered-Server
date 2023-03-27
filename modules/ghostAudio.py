#
# Paul's Extreme Sound Stretch (Paulstretch) - Python version
#
# by Nasca Octavian PAUL, Targu Mures, Romania
# http://www.paulnasca.com/
#
# http://hypermammut.sourceforge.net/paulstretch/
#
# this file is released under Public Domain
#


import sys
from numpy import *
import scipy.io.wavfile
import wave
import gtts
from pydub import AudioSegment
import modules.pytools as pytools
import math
import modules.floorplan as floorplan
import pyttsx3
import time

class audio:
    def load_wav(filename):
        try:
            wavedata=scipy.io.wavfile.read(filename)
            samplerate=int(wavedata[0])
            smp=wavedata[1]*(1.0/32768.0)
            if len(smp.shape)>1: #convert to mono
                smp=(smp[:,0]+smp[:,1])*0.5
            return (samplerate,smp)
        except:
            print ("Error loading wav: "+filename)
            return None



    ########################################

    def paulstretch(samplerate,smp,stretch,windowsize_seconds,outfilename):
        outfile=wave.open(outfilename,"wb")
        outfile.setsampwidth(2)
        outfile.setframerate(samplerate)
        outfile.setnchannels(1)

        #make sure that windowsize is even and larger than 16
        windowsize=int(windowsize_seconds*samplerate)
        if windowsize<16:
            windowsize=16
        windowsize=int(windowsize/2)*2
        half_windowsize=int(windowsize/2)

        #correct the end of the smp
        end_size=int(samplerate*0.05)
        if end_size<16:
            end_size=16
        smp[len(smp)-end_size:len(smp)]*=linspace(1,0,end_size)

        
        #compute the displacement inside the input file
        start_pos=0.0
        displace_pos=(windowsize*0.5)/stretch

        #create Hann window
        window=0.5-cos(arange(windowsize,dtype='float')*2.0*pi/(windowsize-1))*0.5

        old_windowed_buf=zeros(windowsize)
        hinv_sqrt2=(1+sqrt(0.5))*0.5
        hinv_buf=hinv_sqrt2-(1.0-hinv_sqrt2)*cos(arange(half_windowsize,dtype='float')*2.0*pi/half_windowsize)

        while True:

            #get the windowed buffer
            istart_pos=int(floor(start_pos))
            buf=smp[istart_pos:istart_pos+windowsize]
            if len(buf)<windowsize:
                buf=append(buf,zeros(windowsize-len(buf)))
            buf=buf*window
        
            #get the amplitudes of the frequency components and discard the phases
            freqs=abs(fft.rfft(buf))

            #randomize the phases by multiplication with a random complex number with modulus=1
            ph=random.uniform(0,2*pi,len(freqs))*1j
            freqs=freqs*exp(ph)

            #do the inverse FFT 
            buf=fft.irfft(freqs)

            #window again the output buffer
            buf*=window


            #overlap-add the output
            output=buf[0:half_windowsize]+old_windowed_buf[half_windowsize:windowsize]
            old_windowed_buf=buf

            #remove the resulted amplitude modulation
            output*=hinv_buf
            
            #clamp the values to -1..1 
            output[output>1.0]=1.0
            output[output<-1.0]=-1.0

            #write the output to wav file
            outfile.writeframes(int16(output*32767.0).tostring())

            start_pos+=displace_pos
            try:
                time.sleep(start_pos / len(smp))
            except:
                pass
            if start_pos>=len(smp):
                print ("100 %")
                break
            sys.stdout.write ("%d %% \r" % int(100.0*start_pos/len(smp)))
            sys.stdout.flush()

        outfile.close()
    ########################################

    # (samplerate,smp)=load_wav("input.wav")

    # paulstretch(samplerate,smp,8.0,0.25,"out.wav")
    
def getVolumes(floor, coords):
    speakers = pytools.IO.getJson("speakers.json")
    volumes = {
        
    }
    floorplan.loadLevel(0)
    for room in speakers:
        for speaker in speakers[room]:
            for location in speakers[room][speaker]:
                print(speaker)
                try:
                    n = floorplan.map.getMuffle(floor, coords[0], coords[1], location[0], location[1])
                    if n < volumes[speaker]:
                        volumes[speaker] = n
                except:
                    volumes[speaker] = (floorplan.map.getMuffle(floor, coords[0], coords[1], location[0], location[1]))
    return volumes

# voice: [((1.3 * random.random()) + 0.3), (random.random() * 10) + 4, random.random()]
def speak(words, name, type, mood, voice, activity=1, coords=[0, 0], floor=0):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 95)
    engine.save_to_file(words, ".\\sound\\assets\\active_ghost." + name + ".wav")
    # gtts.gTTS(text=words, lang="en", slow=False).save(".\\sound\\assets\\active_ghost." + name + ".mp3")
    try:
        sound = AudioSegment.from_file(".\\sound\\assets\\active_ghost." + name + ".wav", format="wav")
        voiceCoeff = (voice[0] + ((random.random() * (mood / 100)) * (2 - type)))
        stretchCoeff = (voice[1] + ((random.random() * (mood / 100)) * (type - 1)))
        windowSize = (voice[2] + ((random.random() * (mood / 100)) * (type - 1)))
        if voiceCoeff < 0.3:
            voiceCoeff = 0.3
        if voiceCoeff > 1.6:
            voiceCoeff = 1.6
        if windowSize > 1:
            windowSize = 1
        new_sample_rate = int((sound.frame_rate * voiceCoeff))
        hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        hipitch_sound = hipitch_sound.set_frame_rate(44100)
        hipitch_sound.export(".\\sound\\assets\\active_ghost." + name + ".wav", format="wav")
        (samplerate, smp) = audio.load_wav(".\\sound\\assets\\active_ghost." + name + ".wav")
        audio.paulstretch(samplerate, smp, stretchCoeff / 1.5, windowSize, ".\\sound\\assets\\active_ghost." + name + ".wav")
        print((5 * random.random()) + math.fabs(mood))
        volumes = getVolumes(floor, coords)
        print(volumes)
        masterVolume = ((activity / 10) * random.random()) + ((math.fabs(mood) / 100) * (activity / 10))
        pytools.sound.main.playSound("active_ghost." + name + ".wav", 0, (50 / (1 + volumes["clock"])) * masterVolume, 1.0, 0.0, 0)
        pytools.sound.main.playSound("active_ghost." + name + ".wav", 1, (50 / (1 + volumes["fireplace"])) * masterVolume, 1.0, 0.0, 0)
        pytools.sound.main.playSound("active_ghost." + name + ".wav", 2, (50 / (1 + volumes["window"])) * masterVolume, 1.0, 0.0, 0)
    except:
        pass


