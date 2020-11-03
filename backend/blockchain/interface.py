import json
from flask import Flask, request, logging
from web3 import Web3


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

w3.eth.defaultAccount = w3.eth.accounts[1]

# Get stored abi and contract_address
with open("data.json", 'r') as f:
    datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

app = Flask(__name__)

# api to set new user every api call
@app.route("/blockchain/candidates", methods=['GET'])
def result():
    # Create the contract instance with the newly-deployed address
    
    candidate_id = request.args.get(["candidate_id"])
    
    election = w3.eth.contract(address=contract_address, abi=abi)
    
    
    count = election.functions.totalVotesFor(Web3.toHex(str.encode(candidate_id))).call()
    
    return json.dumps({candidate_id:count}), 200


@app.route("/blockchain/vote", methods=['POST'])
def vote():
    
    candidate_id = request.form["candidate_id"]
    election = w3.eth.contract(address=contract_address, abi=abi)
    
    election.functions.totalVotesFor(Web3.toHex(str.encode(candidate_id))).call()

    tx_hash = election.functions.voteForCandidate(Web3.toHex(str.encode("A"))).transact()
    
    #receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    #sending transaction hash as receipt
    return json.dumps({"receipt": tx_hash.hex()}), 200


@app.route('/')
def hello():
    return 'Blockchain Service is active'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


if __name__ =="__main__":
    app.run(debug=True,port=5006)

