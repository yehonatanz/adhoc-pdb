import os
import subprocess
import sys
import telnetlib
import time

import pytest

import adhoc_pdb


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


def test_pdb_is_opened(script_path, script, telnet):
    # type: (str, subprocess.Popen, telnetlib.Telnet) -> None
    assert script.stdout.readline() == b"Starting\n"

    script.send_signal(adhoc_pdb.DEFAULT_SIGNAL)
    remote_pdb_log = script.stderr.readline()
    assert b"waiting for connection" in remote_pdb_log
    assert str(adhoc_pdb.DEFAULT_PORT).encode("utf-8") in remote_pdb_log

    telnet.open("localhost", adhoc_pdb.DEFAULT_PORT)
    banner = telnet.read_until(b"\n(Pdb)", timeout=1)
    assert b"->" in banner
    assert script_path.encode("utf-8") in banner
