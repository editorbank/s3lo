call %~dp0settings.cmd
docker run -it --rm -v "%CD%":"/pwd"  -w "/pwd" --name py2bin-%RANDOM% docker.io/editorbank/py2bin /compile.sh %main_py%