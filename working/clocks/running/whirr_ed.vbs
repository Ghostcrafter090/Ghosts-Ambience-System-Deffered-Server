Set Sound = CreateObject("WMPlayer.OCX.7") 
Sound.URL = "whirr_ed.mp3"
Sound.Settings.Volume = 50
Sound.Controls.play 
do while Sound.currentmedia.duration = 0 
wscript.sleep 100 
loop 
wscript.sleep (int(Sound.currentmedia.duration)+1)*1000 

