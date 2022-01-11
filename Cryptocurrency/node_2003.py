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
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_adress = urlparse(address)
        self.nodes.add(parsed_adress.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for nodes in network:
            response = requests.get(f'http://{nodes}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length>max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# Part 2 - Mining our Blockchain using Postman

# Creating a Web App
app = Flask(__name__)

#creating an adress for a node on port 2000 -- to start the blockchain
# for creating payouts to the miner whenever he mines a block

node_address = str(uuid4()).replace('-','')


# Creating a Blockchain
bainschain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = bainschain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = bainschain.proof_of_work(previous_proof)
    previous_hash = bainschain.hash(previous_block)
    bainschain.add_transaction(sender = node_address, reciever = 'bains', amt = 10)
    block = bainschain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

#adding a transaction to the blockchain to be mined
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = {'sender','reciever','amt'}
    if not all(key in json for key in transaction_keys):
        return 'not all elements of the transaction are present', 400
    index = bainschain.add_transaction(json['sender'], json['reciever'], json['amt'])
    response = {'message': f'The transanction is successful and recievd in the block {index}'}
    return jsonify(response), 201

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

@app.route('/add_nodes', methods = ['POST'])
def add_nodes():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "no node", 401
    for node in nodes:
        bainschain.add_node(node)
    response = {'message':'The nodes are successfully added. The total nodes are :',
                'total nodes': list(bainschain.nodes)}
    return jsonify(response), 201
 
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = bainschain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Chain replaced',
                    'new chain': bainschain.chain}
    else:
        response = {'message': 'All Good, nothing changed',
                    'new chain': bainschain.chain}
    return jsonify(response), 200


# Running the app
app.run(host = '0.0.0.0', port = 2003)
