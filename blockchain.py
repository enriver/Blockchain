import hashlib
from time import time
import json


class Blockchain(object):
    def __init__(self):
        self.chain=list()
        self.current_transaction=list()

        # Genesis block 생성
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        block={
            'index' : len(self.chain)+1,
            'timestamp' : time(),
            'transactions' : self.current_transaction,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])
        }

        self.current_transaction = list()
        self.chain.append(block)
        
        return block

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transaction
        self.current_transaction.append(
            {
                'sender' : sender,
                'recipient' : recipient,
                'amount' : amount
            }
        )

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a Block
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def pow(self, last_proof):
        proof=0
        
        while self.valid_proof(last_proof, proof) is False:
            proof +=1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof + proof).encode()

        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == '0000'

