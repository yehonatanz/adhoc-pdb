from typing import Union

import pytest

from adhoc_pdb.utils import UnknownSignal, resolve_signum


@pytest.mark.parametrize(
    ("signum", "expected"),
    [
        ("usr1", 10),
        ("USR1", 10),
        ("uSr1", 10),
        ("sigusr1", 10),
        ("SiGusr1", 10),
        ("SIGUSR1", 10),
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
