@echo off
title CareerLens - Backend Server
color 0B

echo =======================================================================
echo                 CAREERLENS BACKEND SERVER (FLASK API)
echo =======================================================================
echo.
echo Initializing Database & Starting Server on http://127.0.0.1:5000...
echo.

python -c "import database; database.create_tables(); print('Database verified and tables initialized.')"
python app.py

pause
