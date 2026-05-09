#!/usr/bin/env python3

import re

error_pattern = re.compile(r'\[[U_]{2,}]')

with open('/proc/mdstat') as f:
    for line in f:
        match = re.search(error_pattern, line)
        if not match or "_" not in match.string:
            continue
        print("--ERROR en RAID--")
        break
    else:
        print("--All RAIDs OK--")

print("--OK Script--")
