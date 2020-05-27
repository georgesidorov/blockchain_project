#!/usr/bin/env python3.7
import os
import sys
from io import StringIO
import logParser
import contractCommunicator as cC
import collections
import collections_extended
import frozendict
import hashlib, uuid
from eth_utils import to_bytes

class logBuffer:
    def __init__(self):
        pass

#   Name: George Sidorov
#   Student number: 15375551
#   Please consult README.md before use.

#logParser.logparser()

old_stdout = sys.stdout
result = StringIO()     #  StringIO is used to redirect stdout to be held into string buffer.
sys.stdout = result

logParser.logparser()   #  Calls logparser function from logParser class.

sys.stdout = old_stdout

bufferstring = result.getvalue()      #  Parsing into buffer string.

lines = bufferstring.split("\n")      #  Splitting parsed string.

print("\nRaw log data was parsed to program buffer.\n")

dx_raw = collections.defaultdict(lambda: collections_extended.bag())   #   Must use multiset/bag which allows for duplicate elements.
dx_logs = {}
dx_hashed = {}

for i in range(0, len(lines)):      #      Organises raw log input to be mapped by timestamp.
    line = lines[i]
    words = line.split()
    timestamp = " ".join(words[:2])
    rest = " ".join(words[2:])
    dx_raw[timestamp].add(rest)
    continue

print("Raw log data was mapped to local log dictionary.\n")

for timestamp, rest in dx_raw.items():                                                                  #   Dictionary comprehension.
    dx_logs = {timestamp: rest for (timestamp, rest) in dx_raw.items() if timestamp and timestamp[0]}   #   Removes entries of type None.
    continue

print("Local log dictionary was cleaned. Entries of type NULL removed.\n")

dx_frozen = frozendict.frozendict(dx_logs)      #   Immutable dictionary.

print("Local log dictionary was made immutable for hashing.\n")

salt = uuid.uuid4().hex   #   Randomly generated salt for adding to hashing algorithm. 32 character length.

for k, v in dx_frozen.items():                                                                        #   Hashing application.
    hashed = hashlib.sha512(repr(dx_frozen[k]).encode('UTF-8') + salt.encode('UTF-8')).hexdigest()    #   SHA512 outputs hash of 128 character length.
    key_bytes = to_bytes(text=k)
    value_bytes = to_bytes(text=hashed)
    dx_hashed.update({key_bytes:value_bytes})
    continue

print("Local log dictionary was hashed for blockchain transfer.\n")
print("...please wait while transfer is conducted.\n")

#  WARNING: The following may take over 10 minutes to transfer log file of full size.
for key, value in dx_hashed.items():                                    #  Transaction makes a modification to the blockchain network.
    tx_hash = cC.smartRetriever.functions.add(key,value).transact()     #  Hash of pending transaction.
    tx_receipt = cC.w3.eth.waitForTransactionReceipt(tx_hash)           #  Once transaction included in block, return receipt.
    continue

print("Transfer complete.\n")
