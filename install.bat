@echo off
set PIPENV_VENV_IN_PROJECT=true

cd %~dp0
pipenv install
call .venv\Scripts\activate
python setup.py build
pause
