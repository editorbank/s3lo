call %~dp0settings.cmd
docker run -it --rm  -v "%CD%":"c:\pwd" -w "c:\pwd" --name py2exe-%RANDOM% editorbank/nuitka-image cmd /c nuitka --onefile %main_py%
