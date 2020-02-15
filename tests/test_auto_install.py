import os
import subprocess
import sys

import pytest


def test_auto_install(uninstall_auto):
    assert os.system("adhoc-pdb auto") == 0
    assert check_installed()


@pytest.yield_fixture
def uninstall_auto():
    try:
        yield
    finally:
        assert os.system("adhoc-pdb auto --remove") == 0
        assert not check_installed()


def check_installed():
    p = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import signal; assert signal.getsignal(signal.SIGUSR1).__module__.startswith('adhoc_pdb.')",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.wait() == 0
