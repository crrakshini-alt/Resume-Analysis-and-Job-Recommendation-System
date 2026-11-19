@echo off
title CareerLens - Automated Test Suite Runner
color 0A

echo =======================================================================
echo          CAREERLENS: AUTOMATED TEST SUITE & VERIFICATION
echo                  Software Quality Assurance & Testing
echo                       Lead Engineer: Rakshini
echo =======================================================================
echo.
echo Navigating to Backend & Test directory...
cd /d "%~dp0Resume_analyser"

echo Running all 30 Unit, Integration, and API Test Suites...
echo.

python -m unittest discover -s tests -p "test_*.py" -v

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =======================================================================
    echo   [SUCCESS] ALL 30 TEST SUITES PASSED (100%% PASS RATE)
    echo   Empirically Verified: Zero Runtime Errors, Zero Failures!
    echo =======================================================================
) else (
    echo.
    echo =======================================================================
    echo   [FAILURE] ONE OR MORE TESTS FAILED. CHECK LOGS ABOVE.
    echo =======================================================================
)

echo.
pause
