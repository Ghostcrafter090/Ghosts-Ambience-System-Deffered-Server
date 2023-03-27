@echo on 
@echo derp > thact.derp 
echo Thunder Storm Sounds Active > thunders.dlst
pushd "%USERPROFILE%\desktop\ambience\working"
start "" "light.exe" thunder_storm_lightning.vbs
timeout /t 12
start "" "clock.exe" thunder_storm.vbs
start "" "windown.exe" thunder_storm.vbs
start /wait "" "fireplace.exe" thunder_storm.vbs
popd
del thunders.dlst /f /s /q
del thact.derp /f /s /q 
exit
