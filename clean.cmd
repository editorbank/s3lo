for %%I in (
  pyz.tmp
  build
  s3lo.egg-info
) do @if exist %%I rd /q /s %%I

for %%I in (
  s3lo-*.whl
  s3lo.pyz
) do @if exist %%I del /q /f %%I
