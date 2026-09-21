@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo Compiling all LaTeX files recursively
echo ========================================

for /r %%F in (*.tex) do (
    echo.
    echo ----------------------------------------
    echo Trying: %%F
    echo ----------------------------------------

    pushd "%%~dpF"

    latexmk -pdf -interaction=nonstopmode -halt-on-error "%%~nxF" >nul 2>&1

    if !errorlevel! equ 0 (
        echo [SUCCESS] %%F
    ) else (
        echo [SKIPPED] %%F
    )

    popd
)

echo.
echo ========================================
echo Finished.
echo ========================================

pause