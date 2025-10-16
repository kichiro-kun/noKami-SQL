@echo off

REM Run Test Config
set isUseENV=false
set isPrepareMySQL=true

REM PATH Config
set VirtualEnvPATH=".\.venv\Scripts\activate.bat"

REM MySQL Config
set USER="root"
set HOST="127.0.0.1"
set PORT="3333"
set QueryPATH=".\tests\test_boundary\sql_queries\prepare_database.sql"

REM -------------------------------------------------------------------------------------

REM Activate the virtual environment at *CMD*
IF %isUseENV%==true (
        call %VirtualEnvPATH%
)

REM Check the *coverage* library
pip show coverage >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo The *coverage* library is not installed in active environment.
    echo Please, install it uses next command at your environment: `pip install coverage`
    exit /b
)

REM Prepare Environment
cd .\project_code

IF %isPrepareMySQL%==true (
    <nul set /p=Prepare MySQL - Query Result:
    mysqlsh --sql -u %USER% -h %HOST% -P %PORT% --file=%QueryPATH%
    echo.
)

REM -------------------------------------------------------------------------------------

REM Run Tests
coverage run --source=. -m unittest discover .\tests\ "test_*.py"
coverage report