import signal
from types import FrameType

from remote_pdb import RemotePdb

DEFAULT_SIGNAL = signal.SIGUSR1
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9999


def install(signum=DEFAULT_SIGNAL, bind_host=DEFAULT_HOST, bind_port=DEFAULT_PORT):
    # type: (int, str, int) -> None
    def _set_trace(received_signum, frame):
        # type: (int, FrameType) -> None
        RemotePdb(host=bind_host, port=bind_port).set_trace(frame)

    signal.signal(signum, _set_trace)


__all__ = ["DEFAULT_SIGNAL", "DEFAULT_HOST", "DEFAULT_PORT", "install"]
