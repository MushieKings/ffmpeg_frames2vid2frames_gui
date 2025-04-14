@echo off

IF NOT EXIST venv (
    echo Creating venv...
    python -m venv venv
)

:: Deactivate the virtual environment
call .\venv\Scripts\deactivate.bat

call .\venv\Scripts\activate.bat

:: Upgrade pip
python.exe -m pip install --upgrade pip

pip install -r requirements.txt
pause