#!/usr/bin/env python3.7
import sys
import time
import hashlib
from eth_utils import to_bytes
from logBuffer import dx_frozen, salt
import contractCommunicator as cC

class logRetriever:
    def __init__(self):
        pass

#   Name: George Sidorov
#   Student number: 15375551
#   Please consult README.md before use.

keylist = list(dx_frozen.keys())   #   Used to check if input given by user is valid, also to provide lower and upper range threshold.

print("Initiating retrieval of logs.")

while True:
    try:        #       Asking user for input until they give a valid response.
        fromstr = input("\nPlease follow format for input such as '10.30 16:49:06'\n"   # Example provided is the first timestamp.
                        "Please enter START of timestamp range "
                        "for log retrieval:")

        bracketisedfrom = "[" + fromstr + "]"       #    Add brackets much like timestamp is found in log data.
        lower = keylist.index(bracketisedfrom)      #    Specify lower range threshold.

        tostr = input("\nPlease follow format for input such as '07.27 10:32:36'\n"    # Example provided is the last timestamp.
                        "Please enter END of timestamp range "
                        "for log retrieval:")

        bracketisedto = "[" + tostr + "]"
        upper = keylist.index(bracketisedto)       #    Specify upper range threshold.
        upper += 1
    except ValueError:
        print("Sorry, invalid input. Please try again.")
        continue

    print("\nPrinting logs in 3 seconds...\n")
    time.sleep(3)

    rangelist = keylist[lower:upper]

    for i in range(len(rangelist)):
        current_key = rangelist[i]
        current_key_bytes = to_bytes(text=current_key)

        hash_to_check = hashlib.sha512(repr(dx_frozen[current_key]).encode('UTF-8') + salt.encode('UTF-8')).hexdigest()
        hash_to_check_bytes = to_bytes(text=hash_to_check)  #  Reproducing the hash is most secure to ensure integrity of data.

        value_at_current_key = dx_frozen[current_key]   #   Items found at current key in multiset/bag.
        value_lines = list(value_at_current_key)        #   Convert items to readable list.

        contained_bool = cC.smartRetriever.functions.contains(current_key_bytes).call()

        if contained_bool: #   If current key exists in blockchain: Check if reproduced hash corresponds to hash stored in blockchain.
            if hash_to_check_bytes == cC.smartRetriever.functions.getByKey(current_key_bytes).call():
                for j in range(0, len(value_lines)):
                    timestamp_to_output_for_each_line = str({current_key})[2:-2]
                    print(timestamp_to_output_for_each_line + " " + value_lines[j])   #   Replicate and output log data.
                    continue
            else:
                time.sleep(2)
                sys.exit("ERROR: Local log records may have been tampered with.")
        else:
            time.sleep(2)
            sys.exit("ERROR: Local log records may have been tampered with.")
        continue
    break