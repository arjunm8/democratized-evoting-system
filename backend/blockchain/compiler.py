import json
from web3 import Web3
from solcx import compile_files
# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


listOfCandidates = ['A', 'B', 'C']

hex_array = [Web3.toHex(str.encode(bytes_data)) for bytes_data in listOfCandidates] 


def deploy_contract(contract_interface):
    
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor(hex_array).transact({'from': w3.eth.accounts[1]})

    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address

# compile all contract files
contracts = compile_files(['x.sol'])
# separate main file and link file
main_contract = contracts.pop("x.sol:Election")
 

with open('data.json', 'w') as outfile:
    data = {
        "abi": main_contract['abi'],
        "contract_address": deploy_contract(main_contract)
    }
    json.dump(data, outfile, indent=4, sort_keys=True)
    
