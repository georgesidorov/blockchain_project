#!/usr/bin/env python3.7
import sys
import time

fileloc = "Proxifier.log" 

#   Name: George Sidorov
#   Student number: 15375551
#   Please consult README.md before use.

def logparser():
    with open(fileloc, "r") as f:
        lines = f.readlines()
        temp = list()             #   Temporary list for holding groupings of logs.

        try:
            for i in range(0, len(lines)):
                line = lines[i]
                nextline = lines[i + 1]
                prevline = lines[i - 1]         #  In the following code, 'line[1:15]' is the location of a timestamp in a given log.
                if line[1:15] != nextline[1:15] and line[1:15] != prevline[1:15]:  #  Check for singular logs with non-repeated timestamp.
                    temp.append(line)
                    sys.stdout.write(" " + "\n")
                    sys.stdout.write("".join(temp))
                    del temp[:]
                    #time.sleep(1)
                elif line[1:15] != nextline[1:15]:      #   If the timestamp of 'nextline' does not correspond with current group.
                    temp.append(line)
                    sys.stdout.write(" " + "\n")
                    sys.stdout.write("".join(temp))
                    del temp[:]
                    #time.sleep(1)
                else:
                    temp.append(line)
                continue 
        except IndexError:              #   Given that 'nextline = lines[i + 1]' might not exist:
            temp.append(lines[-1])      #   Append the last line of log data.
        finally:
            sys.stdout.write(" " + "\n")
            sys.stdout.write("".join(temp))
            del temp[:]

class logParser:
    def __init__(self):
        pass
