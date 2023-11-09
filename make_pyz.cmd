@call %~dp0clean.cmd

if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat && echo on
if not exist pyz.tmp pip install -r requirements.txt -t pyz.tmp
if not exist s3lo-*.whl pip wheel .
if exist s3lo-*.whl for %%I in ( s3lo-*.whl ) do pip install %%I -t pyz.tmp
python -c "import zipapp" || pip install zipapps
::copy __main__.py  pyz.tmp\
for /F "usebackq" %%I in ( `dir /b /s pyz.tmp\*.pyc` ) do @del /q /f %%I
for /F "usebackq" %%I in ( `dir /b /s pyz.tmp\*.dist-info` ) do @rd /q /s %%I
if exist pyz.tmp\bin @rd /q /s pyz.tmp\bin
python -m zipapp pyz.tmp -o s3lo.pyz -m s3lo.__main__:main -p interpreter -c && rd /q /s pyz.tmp