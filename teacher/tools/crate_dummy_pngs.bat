@echo off
setlocal

set "LIST=file_names.txt"
set "OUTPUT=dummy_pngs"

if not exist "%OUTPUT%" mkdir "%OUTPUT%"

for /f "usebackq delims=" %%F in ("%LIST%") do (
    type nul > "%OUTPUT%\%%F"
)

echo Done.
pause