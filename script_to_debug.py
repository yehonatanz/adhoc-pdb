import sys
import time

import adhoc_pdb

adhoc_pdb.install()
print("Starting")
sys.stdout.flush()
while True:
    time.sleep(0.01)
print("Done")
sys.stdout.flush()
