@call %~dp0in_venv.cmd
@if exist .whl exit /b 0
@echo Make wheel ...
pip wheel -w .whl .
