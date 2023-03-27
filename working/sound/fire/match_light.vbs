Set Sound = CreateObject("WMPlayer.OCX.7") 
Sound.URL = "match_light.mp3"
Sound.Settings.Volume = 50
Sound.Settings.Rate = 1.0
Sound.Controls.play 
do while Sound.currentmedia.duration = 0 
wscript.sleep 100 
loop 
wscript.sleep (int(Sound.currentmedia.duration)+1)*1000 

