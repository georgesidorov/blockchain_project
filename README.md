# A Lightweight Blockchain-based Solution for Auditable Software
University College Dublin

Module: COMP30910-FYP

Student number: 15375551

Name: George Sidorov

Supervisor: Liliana Pasquale

---

## Project description:

This project is a study of how blockchain technology may be used to ensure the integrity of log records.

It consists of classes that are able to parse log data, 
emulate the behaviour of a logger in real time, 
organise and map each log with respective timestamp, 
hash log entries using a salted SHA-512 algorithm, 
transfer this over the blockchain network on the Ethereum platform, 
and lastly, retrieve log records on the blockchain to compare with local log records, to verify whether logs were tampered with.

---

## File contents of project:

1. `logParser.py`
2. `logBuffer.py`
3. `logRetriever.py`
4. `contractCommunicator.py`
5. `smartRetriever.sol`
6. `2_deploy_contracts.js`
7. `truffle-config.js`
8. `Proxifier.log`
9. `README.md`

## Versions of software the project was conducted on:
1. Node v12.16.3
2. npm v6.14.5
3. Truffle v5.1.26
4. Solidity v0.5.16
5. Node v12.16.3
6. Python v3.7.7
7. pip v20.1.1
8. OS: Ubuntu 18.04.4 LTS

## Versions of pypi.<span>org packages used:
1. Web3.<span>py v5.10.0
2. collections-extended v1.0.3
3. frozendict v1.2
4. eth-utils v1.9.0

---

## Instructions for configuration of project environment:

Open terminal and create folder for project:
>mkdir blockchain_project

>cd blockchain_project

Make sure truffle was installed and input within new directory:
>truffle init

The result is an unboxing of 3 folders (contracts, migrations, test) and file 'truffle-config.js'.

contracs/ and migrations/ already contain a file in each folder. 
Do not touch!

Now, copy the code into the truffle framework.

1. Copy `smartRetriever.sol` into blockchain_project/contracts/
2. Copy `2_deploy_contracts.js` into blockchain_project/migrations/
3. Copy `logParser.py`, `logBuffer.py`, `logRetriever.py` into blockchain_project/
4. Copy `contractCommunicator.py` into blockchain_project/
5. Copy `Proxifier.log` into blockchain_project/
6. Replace `truffle-config.js` in blockchain_project/ with our `truffle-config.js`

Now, return to the terminal and input:
> truffle develop

This opens the develop console. Please take note of YOUR address shown after input such as:
> Truffle Develop started at ht<span>tp://127.0.0.1:7545/

Now, open file `truffle-config.js` in text editor of your choice.
Edit fields host and port according to YOUR host and port and save.
> host: "127.0.0.1"

> port: 7545

Return to truffle develop console and input the following:
> compile

> migrate

Once migrate is complete, under headings <ins>2_deploy_contracts.js</ins> and <ins>Deploying 'smartRetriever'</ins> copy YOUR contract address such as:
> contract address:    0xe9935417CebA109eE0C97BAebeD63F489F1Ea07b

Now, open file `contractCommunicator.py` in text editor.
Edit field blockchain_address to specify YOUR blockchain address such as:
> blockchain_address = 'ht<span>tp://127.0.0.1:7545'

and field deployed_contract_address to specify YOUR contract address such as:
> deployed_contract_address = '0xe9935417CebA109eE0C97BAebeD63F489F1Ea07b'

Hit save, you are now ready to run the project.

Now, open another terminal in blockchain_project/ and execute `logRetriever.py` with command:
> python3 logRetriever.<span>py

---

# IMPORTANT! Things to note about each class:

## Log Parser

The logParser class features the logparser() function.
The logparser() function compares the current line, the next line and the previous line to identify groups of logs by their timestamp.

To emulate the behaviour of a logger in real time, it would be in the interest of future users to uncomment the 2 lines of code '#time.sleep(1)', to have a one second delay between groups of logs which share the same timestamp. 
This creates a very long time to parse the data, but the option is there if you would like.
If you were to uncomment these 2 lines, the logger would log the data in real time but it would not be visible in terminal. 
To make it visible, uncomment line of code '#logParser.logparser()' at the top of the logBuffer class. 
Please read further in the logBuffer class section for more details.


## Log Buffer

Uncommenting the code '#logParser.logparser()' can be used to emulate a logger.
The only purpose of this line of code is to output to terminal.
It is the code after '#logParser.logparser()' which calls the function again and stores output in buffer.

If logParser and logBuffer have had '#time.sleep(1)' and '#logParser.logparser()' lines uncommented, this means that a user would have to wait the same duration of time once again after logparser() outputs log groups to terminal, for logparser() to then output to stdout to be stored in buffer. 
If testing with `Proxifier.log` data of full size, it contains 5457 unique log timestamp groups which would mean that a user would have to wait 90 minutes for logs to be displayed in terminal, and 90 minutes once again for it to be stored in buffer.

If a future user decides that they wish to emulate the behaviour of a logger, having had those 3 lines of code uncommented, they will notice that their data is being outputed to terminal with a '\n' newline character after each group of logs.

The code responsible for this newline character can be found in the logParser class.

The reason for this implementation was for user readability when emulating a logger in real time, to more easily recognise that logs are being outputted to their corresponding timestamp group.

The logBuffer class organises the raw output into a dictionary called 'dx_raw'. 
This also means that each newline character is put into the dictionary with entry of type None. 
The logBuffer class copies the contents of 'dx_raw' using a dictionary comprehension to a new dictionary called 'dx_logs', but without the entries of type None. This dictionary is then made immutable and stored as 'dx_frozen'. 
It is prepared for hashing. 
A random salt of 32 character length is generated, to be added to the SHA-512 hashing algorithm for each value that can be found at given key in 'dx_frozen'. 
The hashed dictionary 'dx_hashed' is then transfered to the blockchain network and stored in mapping.

## Log Retriever

The logRetriever class asks the user to specify a time range of timestamp.
A user may have to inspect the `Proxifier.log` data first to decide which time range they would like, as any input that is not contained in the list of timestamps is not accepted.

The START and END prompt which asks user to input a timestamp range feature an example of the first and last timestamp that can be found in `Proxifier.log` data.
Use this at your disposal.

The logs are printed if they satisfy the following conditions:
Check to see if the current key is contained in the blockchain.
If it is, then the hash is recreated for the logs of current key stored locally and compared to the hash that can be found on the blockchain at given current key.

If the conditions are not met, the program terminates with the following ERROR code:

> ERROR: Local log records may have been tampered with.

This is an ambiguous error code and does not differentiate whether the timestamp or hash is wrong, to prevent any malicious tamperers of using this information to their advantage.

---

## Data used in project:

The data of `Proxifier.log` was provided to us by the Logpai group.

It is a log of the Proxifier software program used by network applications to assist in the use of proxy servers.

It can be found at following link:

https://github.com/logpai/loghub

Scroll down and click Proxifier under **Standalone software** heading.

Note: data provided here is only a sample version.

Please follow Zenodo link found there to download logs of full size, also included:

https://zenodo.org/record/3227177

---

## Acknowledgements:

Liliana Pasquale for providing excellent guidance that was most helpful for project development. Thank you!

The Ubuntu operating system.

Charles Babbage.

---
