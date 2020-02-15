import errno
import os
import shutil
import site
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


@click.group()
def cli():
    pass


@cli.command("debug", help="Debug a python process that installed adhoc_pdb")
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
def cli_debug(ctx, pid, signum, port):
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


PTH_FILE_NAME = "adhoc-pdb-auto-install.pth"
LOAD_LAST_PREFIX = "zzz-"
PTH_FILE_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), PTH_FILE_NAME)
PTH_FILE_DST = os.path.join(site.getsitepackages()[0], LOAD_LAST_PREFIX + PTH_FILE_NAME)


@cli.command("auto", help="Makes adhoc-pdb auto install itself on every python process")
@click.option(
    "--remove",
    is_flag=True,
    help="Removes auto install, adhoc-pdb will no longer auto install itself",
)
@click.pass_context
def auto(ctx, remove):
    # type: (click.Context, bool) -> None
    if remove:
        click.echo("Removing auto install")
        try:
            os.remove(PTH_FILE_DST)
        except OSError as e:
            if e.errno == errno.ENOENT:
                click.echo("Nothing to do")
            else:
                raise
        else:
            click.echo("Removed {!r}".format(PTH_FILE_DST))
    else:
        click.echo("Copying {!r} to {!r}".format(PTH_FILE_SRC, PTH_FILE_DST))
        shutil.copy(PTH_FILE_SRC, PTH_FILE_DST)


if __name__ == "__main__":
    cli()
