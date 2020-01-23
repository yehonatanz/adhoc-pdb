import os
import subprocess
import sys
import telnetlib
import time

import pytest


@pytest.fixture(scope="session")
def script_path():
    # type: () -> str
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "script_to_debug.py",
    )
    assert os.path.exists(path)
    return path


@pytest.yield_fixture
def script(script_path):
    proc = subprocess.Popen(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    try:
        time.sleep(0.1)
        yield proc
    finally:
        proc.terminate()
        time.sleep(0.002)
        if proc.poll() is None:
            proc.kill()


@pytest.yield_fixture
def telnet():
    t = telnetlib.Telnet()
    try:
        yield t
    finally:
        t.close()
