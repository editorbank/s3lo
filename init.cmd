@call %~dp0run.cmd if exist .\requirements.txt if defined VIRTUAL_ENV pip install -r .\requirements.txt
