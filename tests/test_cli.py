from typing import Union

import click
import pytest

from adhoc_pdb.cli import UnknownSignal, cli, resolve_signum


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


def test_cli_fails_on_wrong_signum():
    with pytest.raises(click.UsageError) as e:
        click.Context(cli).invoke(cli, signum="bla")
    assert "bla" in str(e).lower()


def test_cli_fails_on_wrong_pid():
    pid = 123456789
    with pytest.raises(click.UsageError) as e:
        click.Context(cli).invoke(cli, pid=pid)
    assert str(pid) in str(e)
