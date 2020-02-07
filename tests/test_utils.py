import signal
from typing import Union

import pytest

from adhoc_pdb.utils import UnknownSignal, resolve_signum


@pytest.mark.parametrize(
    ("signum", "expected"),
    [
        ("usr1", signal.SIGUSR1),
        ("USR1", signal.SIGUSR1),
        ("uSr1", signal.SIGUSR1),
        ("sigusr1", signal.SIGUSR1),
        ("SiGusr1", signal.SIGUSR1),
        ("SIGUSR1", signal.SIGUSR1),
        ("10", 10),
        (10, 10),
    ],
)
def test_resolve_signum_on_valid_signals(signum, expected):
    # type: (Union[int, str], int) -> None
    assert resolve_signum(signum) == expected


@pytest.mark.parametrize("signum", ["usr", "bla", "1111", 1111, -9, "-9", None])
def test_resolve_signum_on_invalid_signals(signum):
    # type: (Union[str, int]) -> None
    with pytest.raises(UnknownSignal):
        resolve_signum(signum)
