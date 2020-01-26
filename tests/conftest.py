import contextlib
import os
import subprocess
import sys
import telnetlib
import time
from typing import Iterator, List

import pytest

from adhoc_pdb import cli


@pytest.fixture(scope="session")
def root_path():
    # type: () -> str
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert os.path.isdir(path)
    return path


@pytest.fixture(scope="session")
def script_path(root_path):
    # type: (str) -> str
    path = os.path.join(root_path, "script_to_debug.py")
    assert os.path.exists(path)
    return path


@contextlib.contextmanager
def process_fixture(args, startup_time=0.1, time_before_sigkill=0.1):
    # type: (List[str], float, float) -> Iterator[subprocess.Popen]
    proc = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
    )
    time.sleep(startup_time)
    try:
        yield proc
    finally:
        proc.terminate()
        if proc.poll() is None:
            time.sleep(time_before_sigkill)
        if proc.poll() is None:
            proc.kill()


@pytest.yield_fixture
def script(script_path):
    with process_fixture([sys.executable, script_path]) as proc:
        yield proc


@pytest.yield_fixture
def cli_client(script):
    with process_fixture([sys.executable, "-m", cli.__name__, str(script.pid)]) as proc:
        yield proc


@pytest.yield_fixture
def telnet():
    t = telnetlib.Telnet()
    try:
        yield t
    finally:
        t.close()
