@echo on 
@echo derp > thact.derp
echo Thunder Heat Sounds Active > thunder.dlst
pushd "%USERPROFILE%\desktop\ambience\working"
start "" "light.exe" thunder_heat_lightning.vbs
timeout /t 12
start "" "windown.exe" thunder_heat.vbs
start "" "clock.exe" thunder_heat.vbs
start /wait "" "fireplace.exe" thunder_heat.vbs
popd
del thunder.dlst /f /s /q
del thact.derp /f /s /q 
exit 

