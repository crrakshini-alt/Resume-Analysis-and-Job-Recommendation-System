@echo off
title CareerLens - Automated Test Suite Runner
color 0A

echo =======================================================================
echo          CAREERLENS: AUTOMATED TEST SUITE & VERIFICATION
echo                  Software Quality Assurance & Testing
echo =======================================================================
echo.
echo Running all Unit, Integration, and API Test Suites...
echo.

python -m unittest discover -s tests -p "test_*.py" -v

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =======================================================================
    echo   [SUCCESS] ALL TEST SUITES PASSED (100%% PASS RATE)
    echo   System is Verified, Robust, and Ready for Deployment!
    echo =======================================================================
) else (
    echo.
    echo =======================================================================
    echo   [FAILURE] ONE OR MORE TESTS FAILED. CHECK LOGS ABOVE.
    echo =======================================================================
)

echo.
pause
