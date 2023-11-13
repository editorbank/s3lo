@if not exist "%project_name%.pyz" call %~dp0make_pyz.cmd
@call %~dp0settings.cmd

@echo Make exe v2 ...
@setlocal
@if not exist "%project_name%.pyz" ( 1>&2 echo Error: No found "%project_name%.pyz"! & exit /b 1 )
@if exist exe2.tmp.zip del /Q exe2.tmp.zip
@if exist %project_name%.spec del /Q %project_name%.spec
@if exist exe2.tmp rd /Q /S exe2.tmp
@copy %project_name%.pyz exe2.tmp.zip
@powershell -Command "Expand-Archive exe2.tmp.zip -DestinationPath exe2.tmp -Force"
@call %~dp0in_venv.cmd && pip install pyinstaller && pyinstaller exe2.tmp/__main__.py --contents-directory %project_name%.files --name %project_name% && (
  if exist exe2.tmp.zip del /Q exe2.tmp.zip
  if exist %project_name%.spec del /Q %project_name%.spec
  if exist exe2.tmp rd /Q /S exe2.tmp
) && echo OK || ( 1>&2 echo FAIL & exit /b 1 )
@endlocal
