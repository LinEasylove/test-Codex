@echo off
setlocal
cd /d "%~dp0"
echo Installing the pinned local Codex skill collections.
echo Existing same-name skills will not be overwritten automatically.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-Skills.ps1"
set "SKILLS_INSTALL_RESULT=%ERRORLEVEL%"
echo.
if not "%SKILLS_INSTALL_RESULT%"=="0" (
  echo Installation stopped. Read the error above and share it for help.
) else (
  echo Installation finished. Open a NEW local Codex session to check discovery.
)
pause
exit /b %SKILLS_INSTALL_RESULT%
