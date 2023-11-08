if not exist .venv python -m virtualenv .venv
if exist .venv call .venv\Scripts\activate.bat
@set PYTHONPATH=s3lo-0.1.0-py3-none-any.whl;boto-2.49.0-py2.py3-none-any.whl;pyzzer-0.1.1.tar.gz
python -c "import sys;print('\n'.join(sys.path))"
::python -m s3lo --help
::python -m pip install --upgrade pip
::python -m pip wheel .
%*