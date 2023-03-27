del .\clocks\running\wcont.derp /f /s /q

:loop 
if exist .\clocks\running\wcont.derp goto exit 
start /d ".\clocks\running" "..\..\clock.exe" "whirr_cont.vbs"
timeout /t 1
if %time:~3,2% equ 5 goto exit
if %time:~3,2% equ 20 goto exit
if %time:~3,2% equ 35 goto exit
if %time:~3,2% equ 50 goto exit
goto loop 
  
:exit
start /d ".\clocks\running" "..\..\clock.exe" "whirr_ed.vbs"
del .\clocks\running\wcont.derp /f /s /q 
exit 
