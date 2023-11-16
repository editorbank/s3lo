find . -name *.pyc -delete
find . -name __pycache__ -delete
find . -name s3lo.bin -delete
find . -name s3lo.pyz -delete



#@for /F "usebackq" %%I in ( `dir /B /S /A:D __pycache__ 2^>nul` ) do if exist "%%~I" rd /Q /S "%%~I"
#@for /D %%I in (
#  .venv
#  dist
#  build
#  *.tmp
#  *.egg-info
#  *.whl
#) do @(
#  if exist "%%~I" (
#    echo Clean temporary directory "%%~I" ...
#    rd /q /s "%%~I"
#  )
#)
#@for %%I in (
#  *.whl
#  *.pyz
#  exe2.tmp.zip
#) do @(
#  if exist "%%~I" (
#    echo Clean temporary file "%%~I" ...
#    del /q /f "%%~I"
#  )
#)