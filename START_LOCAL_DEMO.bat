@echo off
title CareerLens - Local Demo Server Launcher
color 0B

echo =======================================================================
echo          CAREERLENS: LOCAL OFFLINE DEMONSTRATION SERVER
echo =======================================================================
echo.
cd /d "%~dp0Resume_analyser"

echo [1/2] Verifying SQLite database tables...
python -c "import database; database.create_tables(); print('Database tables verified and ready.')"

echo.
echo [2/2] Starting local Flask server on http://127.0.0.1:5000...
echo.
python app.py

pause
