@echo off
setlocal

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
echo Finished.
echo ========================================

pause

exit /b

:compile
echo.
echo ----------------------------------------
echo Trying: %~1
echo ----------------------------------------

pushd "%~dp1" || (
    echo [SKIPPED] %~1
    exit /b
)

latexmk -pdf -interaction=nonstopmode -halt-on-error "%~nx1" >nul 2>&1
if errorlevel 1 (
    echo [SKIPPED] %~1
) else (
    echo [SUCCESS] %~1
)
popd
exit /b
