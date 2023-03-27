:loop
for /f "tokens=2 delims=:" %%a in ('powershell -command "Get-MpPreference" ^| bash -c "grep -e \"DisableRealtimeMonitoring\""') do (
	if "$%%a"=="$ False" (
		powershell -command "Set-MpPreference -DisableRealtimeMonitoring 0"
	)
)
timeout /t 10
goto loop