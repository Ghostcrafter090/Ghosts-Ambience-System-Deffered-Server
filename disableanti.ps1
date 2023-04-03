While ($true) {
	echo "Setting MpPreference..."
	Set-MpPreference -DisableRealtimeMonitoring 1
	Start-Sleep -Seconds 10
}