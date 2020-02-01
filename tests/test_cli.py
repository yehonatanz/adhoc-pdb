from typing import TypeVar
from typing.io import IO

import click
import pytest

from adhoc_pdb.cli import cli


def test_cli_fails_on_wrong_signum():
    with pytest.raises(click.UsageError) as e:
        click.Context(cli).invoke(cli, signum="bla")
    assert "bla" in str(e.value).lower()


def test_cli_fails_on_wrong_pid():
    pid = 123456789
    with pytest.raises(click.UsageError) as e:
        click.Context(cli).invoke(cli, pid=pid)
    assert str(pid) in str(e.value)


T = TypeVar("T", str, bytes)


def _read_until(buf, pattern):
    # type: (IO[T], T) -> T
    c = buf.read(1)
    while not c.endswith(pattern):
        c += buf.read(1)
    return c


def test_cli_happy_flow(script, script_path, cli_client):
    assert script_path.encode("utf-8") in cli_client.stdout.readline()
    _read_until(cli_client.stdout, b"(Pdb) ")
    cli_client.stdin.write(b"b 10\n")
    cli_client.stdin.flush()
    breakpoint_response = cli_client.stdout.readline()
    assert b"Breakpoint 1 at" in breakpoint_response
    assert breakpoint_response.strip().endswith(b".py:10")
