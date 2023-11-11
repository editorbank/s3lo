@if defined VIRTUAL_ENV exit /b 0
@call %~dp0settings.cmd
@if not exist %venv_dir% (
  echo Create virtual environment ....
  python -m virtualenv %venv_dir% || python -m venv %venv_dir% || exit /b 1
)
@if not exist "%venv_dir%\Scripts\activate.bat" (1>&2 echo Error: Not found "%venv_dir%\Scripts\activate.bat"! & exit /b 1)
@echo Activate virtual environment ....
@call "%venv_dir%\Scripts\activate.bat"
@%*