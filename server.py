from flask import Flask, request, jsonify
from blockchain import Blockchain
import uuid

app=Flask(__name__)
node_identifier = str(uuid.uuid4()).replace('-','')
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def full_chain():
    response={
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender','recipient','amount']

    if not all(k in values for k in required):
        return 'missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )
    response = {'message' : 'Transaction will be added to Block {%s}' % index}

    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():    
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.pow(last_proof)

    blockchain.new_transaction(
        sender='0',
        recipient = node_identifier,
        amount = 1
    )
    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message' : 'new block found',
        'index' : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash']
    }

    return jsonify(response), 200


if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
