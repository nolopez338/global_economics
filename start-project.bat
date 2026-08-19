@echo off
cd /d "%~dp0"

start "Local Project Server" cmd /k "py -m http.server 8000"

timeout /t 2 /nobreak >nul
start "" "http://localhost:8000/index.html"

exit /b