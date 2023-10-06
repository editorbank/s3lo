call %~dp0settings.cmd
if not exist %venv_dir% python -m virtualenv %venv_dir%
if exist %venv_dir%\Scripts\activate.bat call %venv_dir%\Scripts\activate.bat
@if exist %venv_dir%\Scripts\dotenv.exe set _dotenv_run_=dotenv run 
if not defined _dotenv_run_ if exist .env for /F "usebackq" %%I in ( `findstr /V /B "#" .env` ) do set %%I
if /I ""=="%~1" (%_dotenv_run_%python %main_py% & exit /b %ERRORLEVEL%)
if /I ".py"=="%~x1" (%_dotenv_run_%python %~1 & exit /b %ERRORLEVEL%)
%*
