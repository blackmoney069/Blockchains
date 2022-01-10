import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):    #this function creates a block, only after mining that block
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self): 
        return self.chain[-1]

    def proof_of_work(self, previous_proof):  #finds the proof of the work that will be called as mining the block
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):  #hashing fuction to check the validity of the chain
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender,reciever,amt):
        self.transactions.append({'sender':sender,'reciever':reciever,'amt':amt})
        index = self.get_previous_block['index']+1
        return index

    def add_node(self, address):
        parsed_adress = urlparse(address)
        self.nodes.add(parsed_adress.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = length(self.chain)
        for nodes in network:
            response = requests.get(f'http://{node}/get_chain')


# Part 2 - Mining our Blockchain using Postman

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
bainschain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = bainschain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = bainschain.proof_of_work(previous_proof)
    previous_hash = bainschain.hash(previous_block)
    block = bainschain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': bainschain.chain,
                'length': len(bainschain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = bainschain.is_chain_valid(bainschain.chain)
    if is_valid:
        response = {'message': 'valid'}
    else:
        response = {'message': 'Not valid'}
    return jsonify(response), 200

# here we will decentralise the blockchain to nodes



# Running the app
app.run(host = '0.0.0.0', port = 2000)
