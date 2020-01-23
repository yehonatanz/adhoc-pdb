import subprocess
import telnetlib

import adhoc_pdb


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

    telnet.write(b"b 10\n")
    breakpoint_response = telnet.read_until(b"\n(Pdb)", timeout=1)
    assert b"Breakpoint 1 at" in breakpoint_response
    assert breakpoint_response.strip().endswith(b":10\r\n(Pdb)")
