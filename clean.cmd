
@for /D %%I in (
  .venv.?
  pyz.tmp.?
  build.?
  *.egg-info
  *.whl
) do @(
  @echo Clean temporary directory %%I ...
  rd /q /s %%I
)
@for %%I in (
  *.whl
  *.pyz
) do @(
  @echo Clean temporary file %%I ...
  del /q /f %%I
)