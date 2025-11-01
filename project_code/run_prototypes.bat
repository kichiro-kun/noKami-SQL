@echo off

REM Run Test Config
set isPrepareMySQL=true

REM MySQL Config
set USER="root"
set HOST="127.0.0.1"
set PORT="3333"
set QueryPATH=".\prototyping\sql_queries\prepare_mysql_database.sql"

REM -------------------------------------------------------------------------------------

IF %isPrepareMySQL%==true (
    <nul set /p=Prepare MySQL - Query Result:
    mysqlsh --sql -u %USER% -h %HOST% -P %PORT% --file=%QueryPATH%
    echo.
)

REM -------------------------------------------------------------------------------------

REM Run Tests
python .\prototyping_main.py