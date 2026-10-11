"""Offline regression runner; supports Windows managed workspace permissions.

Run from the repository root: .venv/Scripts/python.exe docs/agents/run_checks.py
Only test temporary directories inherit workspace ACLs. No application or
system security settings are changed. Every execution uses a fresh directory.
"""
import os
from pathlib import Path
import sys
import tempfile
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
runtime = ROOT / ".test-runtime"
runtime.mkdir(exist_ok=True)
os.environ["TMP"] = os.environ["TEMP"] = str(runtime)
tempfile.tempdir = str(runtime)
if os.name == "nt":
    original_mkdir = os.mkdir

    def workspace_test_mkdir(path, mode=0o777, *, dir_fd=None):
        resolved = Path(path).resolve()
        if resolved.is_relative_to(runtime) and mode == 0o700:
            mode = 0o777  # Inherit existing ACLs instead of creating owner-only ACLs.
        return original_mkdir(path, mode, dir_fd=dir_fd)

    os.mkdir = workspace_test_mkdir

import pytest
raise SystemExit(pytest.main(["-q", "-p", "no:cacheprovider", "--basetemp=" + str(runtime / ("pytest-" + uuid4().hex)), *(sys.argv[1:] or ["tests"])]))
