import errno
import os
import sys
import telnetlib
import time
from typing import Union

import click

from .adhoc_pdb import DEFAULT_PORT, DEFAULT_SIGNAL
from .utils import UnknownSignal, resolve_signum


def debug(pid, signum=DEFAULT_SIGNAL, port=DEFAULT_PORT):
    # type: (int, int ,int) -> None
    os.kill(pid, signum)
    if sys.version_info < (3, 6):
        time.sleep(0.1)
    telnet = telnetlib.Telnet("localhost", port)
    try:
        telnet.interact()
    finally:
        telnet.close()


@click.command(help="Debug a python process that installed adhoc_pdb")
@click.argument("pid", type=int)
@click.option(
    "-s",
    "--signum",
    help="The signal to send to the process. Either number (10) or name (USR1/SIGUSR1)",
    default=DEFAULT_SIGNAL,
    show_default=True,
)
@click.option(
    "-p",
    "--port",
    type=int,
    help="The telnet port to connect to",
    default=DEFAULT_PORT,
    show_default=True,
)
@click.pass_context
def cli(ctx, pid, signum, port):
    # type: (click.Context, int, Union[str, int], int) -> None
    try:
        signum = int(resolve_signum(signum))
    except UnknownSignal as e:
        ctx.fail(str(e))
    try:
        debug(pid, signum, port)
    except OSError as e:
        if e.errno == errno.ESRCH:
            ctx.fail("No such process {}".format(pid))
        raise


if __name__ == "__main__":
    cli()
