:loop
xcopy \\192.168.2.40\ambience\hosts.json . /c /y
xcopy \\192.168.2.40\ambience\hosts.json .\working /c /y
xcopy \\192.168.2.40\ambience\working\hostData.json .\working /c /y
timeout /t 10
goto loop
