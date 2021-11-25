#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 09:52:21 2021

@author: blackmoney
"""
import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain =[]
        Blockchain.create_block(self, proof=1,prev_hash = '0')
    
    def create_block(self, proof, prev_hash):
        block ={'index':len(self.chain)+1,
                'prev_hash': prev_hash,
                'proof': proof,
                'timestamp': str(datetime.datetime.now())}
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof  = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-prev_proof**2).encode()).hexdigest()
            if hash_operation[0:4]=="0000":
                check_proof = True
            else:
                new_proof+=1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_true(self, chain):
        block_index =1
        prev_block = chain[0]
        while block_index<len(chain):
            #check if the prev_hash condition is satisfied
            block = chain[block_index]
            if block['prev_hash']!= self.hash(prev_block):
                return False
            #CHECK if the proof of work condtion is satisfied
            proof = block['proof']
            prev_proof = prev_block['proof']
            hash_operation = hashlib.sha256(str(proof**2-prev_proof**2).encode()).hexdigest()
            if hash_operation[0:4]!='0000':
                return False
            prev_block = block
            block_index+=1
        return True
            
#mining the blockchain using the Flask Webapp
app = Flask(__name__)

blockchain1 = Blockchain()

@app.route("/mine_block", methods = ["GET"])
def mine_block():
    
            
            
            
            
            
        