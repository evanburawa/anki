# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Helper to run mypy in daemon mode. See development.md. Windows is not
currently supported.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

workspace = Path(os.environ["BUILD_WORKSPACE_DIRECTORY"])
binroot = workspace / ".bazel/bin"
dmypy_bin = binroot / "external/py_deps_mypy/rules_python_wheel_entry_point_dmypy"

if sys.platform.startswith("win32"):
    binext = ".exe"
else:
    binext = ""

if subprocess.run(
    [
        str(dmypy_bin) + binext,
    ]
    + [
        "run",
        "--",
        "--config-file",
        "qt/mypy.ini",
        ".bazel/bin/qt/dmypy.runfiles/ankidesktop/pylib/anki",
        ".bazel/bin/qt/dmypy.runfiles/ankidesktop/qt/aqt",
        "--python-executable",
        os.path.abspath("python/stubs/extendsitepkgs"),
    ],
    env={
        "MYPYPATH": ".bazel/bin/qt/dmypy.runfiles/pyqt6",
        "EXTRA_SITE_PACKAGES": os.path.abspath(os.getenv("EXTRA_SITE_PACKAGES")),
    },
    cwd=workspace,
).returncode:
    sys.exit(1)
