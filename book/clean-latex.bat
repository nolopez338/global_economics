@echo off
echo Hiding LaTeX auxiliary files recursively...

attrib +h /s /d *.aux 2>nul
attrib +h /s /d *.synctex.gz 2>nul
attrib +h /s /d *.log 2>nul
attrib +h /s /d *.out 2>nul

echo Done.
pause