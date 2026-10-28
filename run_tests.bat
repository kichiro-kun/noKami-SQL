@echo off

REM Run Test Config
set isUseENV=true
set isPrepareMySQL=true

REM PATH Config
set VirtualEnvPATH=".\.venv\Scripts\activate.bat"

REM MySQL Config
set USER="root"
set HOST="127.0.0.1"
set PORT="3333"
set QueryPATH=".\project_code\tests\test_boundary\sql_queries\prepare_mysql_database.sql"

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

IF %isPrepareMySQL%==true (

    REM Check the *mysql*
    mysql --version >nul 2>&1

    IF %ERRORLEVEL% NEQ 0 (
        echo *MySQL version check* failed!
        echo Maybe the *mysql* is not installed in active environment!
        exit /b
    )

    <nul set /p=Prepare MySQL - Query Result:
    mysqlsh --sql -u %USER% -h %HOST% -P %PORT% --file=%QueryPATH%
    echo.
)

REM -------------------------------------------------------------------------------------

REM Run Tests
coverage run --source=. -m unittest discover project_code\tests\ "test_*.py"
coverage report