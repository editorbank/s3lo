@call %~dp0make_whl.cmd

@echo Make pyz ...
@setlocal
@set PIP_CONFIG_FILE=
@for %%I in ( .whl\%project_name%-*.whl ) do pip install --no-index -f .whl -t pyz.tmp --no-compile %%I
@endlocal

@python -c "import zipapp" || pip install zipapps
@for /F "usebackq" %%I in ( `dir /b /s pyz.tmp\__pycache__ 2^>nul` ) do @rd /q /s %%I
@for /F "usebackq" %%I in ( `dir /b /s pyz.tmp\*.pyc 2^>nul` ) do @del /q /f %%I
@for /F "usebackq" %%I in ( `dir /b /s pyz.tmp\direct_url.json 2^>nul` ) do @del /q /f %%I
python -m zipapp pyz.tmp -o %project_name%.pyz -m %project_name%.__main__:main -p interpreter -c && rd /q /s pyz.tmp

