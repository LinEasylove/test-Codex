@echo off
setlocal
cd /d "%~dp0"
echo Installing only ppt-master and its isolated Python dependencies.
echo Existing skills will be preserved. This may take several minutes.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-Skills.ps1" -Only ppt-master
set "PPT_MASTER_RESULT=%ERRORLEVEL%"
echo.
if not "%PPT_MASTER_RESULT%"=="0" (
  echo Installation stopped. Read the error above and share it for help.
) else (
  echo Installation completed. Open a NEW local Codex session and check ppt-master.
)
pause
exit /b %PPT_MASTER_RESULT%
