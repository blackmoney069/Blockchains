# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

#create a new blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = [] #added an empty list of transactions to happen
        Blockchain.create_block(self,proof = 1, prev_hash = '0')
        self.nodes = set()
        

    def create_block(self, proof, prev_hash):
        block = {'index':len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'prev_hash':prev_hash,
                 'transactions': self.transactions}
        self.transactions = [] #empty the transaction list 
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-prev_proof**2).encode()).hexdigest()
            if hash_operation[0:4] == '0000':
                check_proof = True
            else:
                new_proof = new_proof+1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block,sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_true(self):
        prev_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block =  chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - prev_proof ** 2).encode()).hexdigest()
            if hash_operation[0:4] != '0000':
                return False
            prev_block = block
            block_index +=1
        return True
    
    def add_transaction (self, sender, reciever, amount):
        self.transactions.append({"sender":sender,
                                  "reciever": reciever,
                                  "amount": amount})
        previous_block = self.get_prev_block()
        return previous_block['index']+1
    
    def add_node(self, node_address):
        parsed_url = urlparse(node_address)
        self.nodes.add(parsed_url.netlock)
    
#mining the blockchain

#creating a webapp for interacting with the blockchain

app = Flask(__name__)

#create a new blockchain

blockchain =  Blockchain()

# mining a new block

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_prev_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message':"congrats!! you just mined a block!",
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'prev_hash':block['prev_hash']
                }
    return jsonify(response),200

# getting the whole blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length':len(blockchain.chain),
                }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    check_chain = blockchain.is_chain_true()
    response = {'message': "The blockchain was checked and wasa found to be "+str(check_chain)}
    return jsonify(response), 200

#decentralising the blockchain


#running the app

app.run(host = '0.0.0.0', port = 5000)







