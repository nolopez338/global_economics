@echo off
cd /d "%~dp0"

start "Magis local server" python -m http.server 8000
timeout /t 2 /nobreak >nul
start "" "http://localhost:8000/teacher/pages/magis.html?access=teacher"
