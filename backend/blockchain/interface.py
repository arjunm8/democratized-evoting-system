import json
from flask import Flask, request, logging
from web3 import Web3
from solcx import compile_files
from models import db, Candidate



w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.defaultAccount = w3.eth.accounts[1]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/evdb"

db.init_app(app)


def deploy_contract(contract_interface,hex_array):

    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor(hex_array).transact({'from': w3.eth.accounts[1]})
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


with app.app_context():
    db.create_all()
    hex_array = [Web3.toHex(str.encode(candidate.get_str_id())) for candidate in Candidate.query.all()] 
    # compile all contract files
    contracts = compile_files(['x.sol'])
    # separate main file and link file
    main_contract = contracts.pop("x.sol:Election")
     
    
    with open('data.json', 'w') as outfile:
        data = {
            "abi": main_contract['abi'],
            "contract_address": deploy_contract(main_contract,hex_array)
        }
        json.dump(data, outfile, indent=4, sort_keys=True)
        
    with open("data.json", 'r') as f:
        datastore = json.load(f)
        abi = datastore["abi"]
        contract_address = datastore["contract_address"]





# api to set new user every api call
@app.route("/blockchain/results", methods=['GET'])
def result():
    # Create the contract instance with the newly-deployed address
    results = []
    election = w3.eth.contract(address=contract_address, abi=abi)
    for candidate in Candidate.query.all():
        c_dict = candidate.serialize()
        c_dict["votes"] = election.functions.totalVotesFor(
                Web3.toHex(
                        str.encode(
                                str(c_dict["id"])
                                )
                        )
                        ).call()
                        
        results.append(c_dict)
        
    return json.dumps({"result":results}), 200


@app.route("/blockchain/vote", methods=['POST'])
def vote():
    candidate_id = request.form["candidate_id"]
    election = w3.eth.contract(address=contract_address, abi=abi)
    
    try:
        tx_hash = election.functions.voteForCandidate(Web3.toHex(str.encode(candidate_id))).transact()
        #receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        #sending transaction hash as receipt
        return json.dumps({"receipt": tx_hash.hex()}), 200
    except:
        return "",403


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

