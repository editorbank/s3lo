
@for /D %%I in (
  .venv
  dist
  build
  *.tmp
  *.egg-info
  *.whl
) do @(
  if exist "%%~I" (
    echo Clean temporary directory "%%~I" ...
    rd /q /s "%%I"
  )
)
@for %%I in (
  *.whl
  *.pyz
  exe2.tmp.zip
) do @(
  if exist "%%~I" (
    echo Clean temporary file "%%~I" ...
    del /q /f "%%~I"
  )
)