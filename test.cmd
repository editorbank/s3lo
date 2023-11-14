if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat && echo on

if exist .env for /F "usebackq tokens=1 delims=#" %%I in ( .env ) do @set %%I
set s3lo=python -m s3lo
if exist s3lo.pyz set s3lo=python s3lo.pyz

%s3lo% list
::%s3lo% upload -f readme.md
::%s3lo% get -k readme.md

	
