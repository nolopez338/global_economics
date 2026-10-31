@echo off
setlocal
cd /d "%~dp0"

echo Updating the local repository...
git pull --rebase
if errorlevel 1 (
  echo ERROR: git pull --rebase failed. No changes were published.
  pause
  exit /b 1
)

git add teacher/assets/js/databases/teacher-tasks.js
if errorlevel 1 (
  echo ERROR: Could not stage teacher-tasks.js.
  pause
  exit /b 1
)

git diff --cached --quiet -- teacher/assets/js/databases/teacher-tasks.js
if errorlevel 2 (
  echo ERROR: Could not inspect the staged teacher task changes.
  pause
  exit /b 1
)
if not errorlevel 1 (
  echo No teacher task changes to publish.
  pause
  exit /b 0
)

git commit -m "Update teacher tasks" -- teacher/assets/js/databases/teacher-tasks.js
if errorlevel 1 (
  echo ERROR: Could not commit the teacher task changes.
  pause
  exit /b 1
)

git push
if errorlevel 1 (
  echo ERROR: The commit was created locally, but git push failed.
  pause
  exit /b 1
)

echo Teacher task changes were synchronized successfully.
pause
exit /b 0
