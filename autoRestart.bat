echo off
set errorCount=0

:loop
py -c "import pytools; pytools.net.getJsonAPI('https://gsweathermore.ddns.net/is_alive.php', timeout=3)" > null
set error=%errorlevel%

if not "$%error%"=="$0" (
   set /a errorCount = %errorCount% + 1
   echo [%date%_%time%] ;;; HTTPS Detected as offline. Current error count: %errorCount%
) else (
   echo [%date%_%time%] ;;; HTTPS is working.
   set errorCount=0
)

if %errorCount% gtr 24 (
    echo [%date%_%time%] ;;; HTTPS detected as broken. Restarting server...
    shutdown /r /t 1
)

timeout /t 10 > null

goto loop