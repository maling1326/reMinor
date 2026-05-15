@echo off
title reMinor Dev Tools

:menu
cls
echo ================================
echo        reMinor Dev Tools
echo ================================
echo 1. Install dependencies
echo 2. Run servers
echo 3. Push to Git
echo 4. Exit
echo ================================
set /p choice="Choose: "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto dev
if "%choice%"=="3" goto upload
if "%choice%"=="4" exit

goto menu

:install
echo Installing frontend dependencies...
call npm install
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..
echo Done!
pause
goto menu

:dev
echo Starting backend...
start cmd /k "cd backend && uvicorn main:app --reload --port 8000"
echo Starting frontend...
start cmd /k "npm run dev"
echo Both servers running!
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
pause
goto menu

:upload
echo Current changes:
git status
set /p message="Commit message: "
git add .
git commit -m "%message%"
git push
echo Done! Pushed to Git.
pause
goto menu