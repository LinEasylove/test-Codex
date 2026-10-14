@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-Skills.ps1" -Verify
set "SKILLS_VERIFY_RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %SKILLS_VERIFY_RESULT%
