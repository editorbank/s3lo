@call %~dp0in_venv.cmd && if exist .\requirements.txt (
  echo Install requirements ...
  pip install -r .\requirements.txt
)