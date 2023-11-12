@if not exist "project.ini" ( 1>&2 echo Error: Not found file "project.ini"! & exit /b 1 )
@for /F "usebackq tokens=1 delims=#" %%I in ( "project.ini" ) do @set %%I
