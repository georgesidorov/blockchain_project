import json
from web3 import Web3, HTTPProvider

class contractCommunicator:
    def __init__(self):
        pass

#   Name: George Sidorov
#   Student number: 15375551
#   Please consult README.md before use.

#  >>truffle develop blockchain address.
blockchain_address = 'http://127.0.0.1:9545'
#  Client instance to interact with the blockchain.
w3 = Web3(HTTPProvider(blockchain_address))
#  Set the default account as to not set the "from" for every transaction call.
w3.eth.defaultAccount = w3.eth.accounts[0]

#  Path to the compiled contract JSON file.
compiled_contract_path = 'build/contracts/smartRetriever.json'

#  Deployed contract address. You must input your address here, see 'migrate' command output: 'contract address'.
deployed_contract_address = '0x55360C440293165FD889e948462dF231645813dE'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # Load contract info as JSON.
    contract_abi = contract_json['abi']  # Load contract's abi, it is necessary to call contract functions.

#  Declare deployed contract reference:
smartRetriever = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)
