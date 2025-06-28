@echo off

REM Activate the virtual environment at CMD
call .\.venv\Scripts\activate.bat

REM Check the coverage library
pip show coverage >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo The *coverage* library is not installed in active virtual environment.
    echo Please, install it uses next command at virtual environment: `pip install coverage`
    exit /b
)

cd .\project_code

coverage run --source=. -m unittest discover .\tests\ "test_*.py"
coverage report