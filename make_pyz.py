# build_app.py

import pathlib
import stat
import zipfile

app_source = pathlib.Path("s3lo/")
app_filename = pathlib.Path("s3lo.pyz")

with open(app_filename, "wb") as app_file:
    # 1. Prepend a shebang line
    shebang_line = b"#!/usr/bin/env python3\n"
    app_file.write(shebang_line)

    # 2. Zip the app's source
    with zipfile.ZipFile(app_file, "w") as zip_app:
        for file in app_source.rglob("*"):
            member_file = file.relative_to(app_source)
            zip_app.write(file, member_file)

# 3. Make the app executable (POSIX systems only)
current_mode = app_filename.stat().st_mode
exec_mode = stat.S_IEXEC
app_filename.chmod(current_mode | exec_mode)