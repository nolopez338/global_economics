@echo off
setlocal

set /a success=0, failed=0, skipped=0 >nul
call :getTime totalStart

echo ========================================
echo Compiling all LaTeX files recursively
echo ========================================

for /r "%~dp0." %%F in (*.tex) do call :compile "%%F"

rem These scaffolds live in the skills tree, outside the year tree.
set "SKILLS_DIR=%~dp0..\.agents\skills"

for %%F in (
    "%SKILLS_DIR%\global-economics-exam\assets\template_exam.tex"
    "%SKILLS_DIR%\global-economics-exam-solution\assets\template_exam_solution.tex"
    "%SKILLS_DIR%\global-economics-home-practice\assets\template_home_practice.tex"
    "%SKILLS_DIR%\global-economics-classroom-activity\assets\template_classroom_activity.tex"
) do call :compile "%%~fF"

echo.
echo ========================================
echo Compilation Summary
echo ========================================
echo Successful: %success%
echo Failed:     %failed%
echo Skipped:    %skipped%

set /a total=success+failed+skipped >nul
echo Total files: %total%
echo ----------------------------------------

call :showElapsed %totalStart% "TOTAL TIME"

echo ========================================
echo Finished.
echo ========================================

pause
exit /b


rem ========================================
rem Compile individual LaTeX file
rem ========================================
:compile
call :getTime fileStart

echo.
echo ----------------------------------------
echo Trying: %~1
echo ----------------------------------------

if not exist "%~1" (
    echo [SKIPPED] %~1
    set /a skipped+=1 >nul
    call :showElapsed %fileStart% "COMPILE TIME"
    exit /b
)

pushd "%~dp1" || (
    echo [SKIPPED] %~1
    set /a skipped+=1 >nul
    call :showElapsed %fileStart% "COMPILE TIME"
    exit /b
)

latexmk -pdf -interaction=nonstopmode -halt-on-error "%~nx1" >nul 2>&1

if errorlevel 1 (
    echo [FAILED] %~1
    set /a failed+=1 >nul
) else (
    echo [SUCCESS] %~1
    set /a success+=1 >nul
)

popd

call :showElapsed %fileStart% "COMPILE TIME"
exit /b


rem ========================================
rem Get current time in centiseconds
rem ========================================
:getTime
set "clock=%time: =0%"

set /a "now=(1%clock:~0,2%-100)*360000 + (1%clock:~3,2%-100)*6000 + (1%clock:~6,2%-100)*100 + (1%clock:~9,2%-100)" >nul

set "%~1=%now%"
exit /b


rem ========================================
rem Calculate and display elapsed time
rem ========================================
:showElapsed
call :getTime endTime

set /a "elapsed=endTime-%~1" >nul

rem Handle midnight rollover
if %elapsed% LSS 0 set /a "elapsed+=8640000" >nul

set /a "hh=elapsed/360000" >nul
set /a "mm=(elapsed%%360000)/6000" >nul
set /a "ss=(elapsed%%6000)/100" >nul
set /a "cc=elapsed%%100" >nul

set "hh=0%hh%"
set "mm=0%mm%"
set "ss=0%ss%"
set "cc=0%cc%"

echo [%~2] %hh:~-2%:%mm:~-2%:%ss:~-2%.%cc:~-2%
exit /b