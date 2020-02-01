import signal
from typing import Union


class UnknownSignal(ValueError):
    pass


def resolve_signum(signum):
    # type: (Union[str, int]) -> int
    if not isinstance(signum, (int, str)):
        raise UnknownSignal(repr(signum))
    elif isinstance(signum, int) or signum.isdigit():
        signum = int(signum)
        try:
            signal.getsignal(signum)
        except ValueError:
            raise UnknownSignal("Unknown signal {}".format(signum))
        else:
            return signum
    else:
        signum = signum.upper()
        if not signum.startswith("SIG"):
            signum = "SIG" + signum
        try:
            return getattr(signal, signum)
        except AttributeError:
            raise UnknownSignal(signum)
