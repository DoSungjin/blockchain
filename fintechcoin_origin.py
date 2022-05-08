from flask import Flask
from flask import request

import json
import requests
import hashlib as hasher
import datetime as date

node = Flask(__name__)


class FTCBlock:
  def __init__(self, index, timestamp, data, prev_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.prev_hash = prev_hash
    self.hash = self.hash_FTCblock()
  
  def hash_FTCblock(self):
    sha = hasher.sha256()
    sha.update((str(self.index) + 
               str(self.timestamp) + 
               str(self.data) + 
               str(self.prev_hash)).encode())
    return sha.hexdigest()





def first_block():
  return FTCBlock(0, date.datetime.now(), {
    "Proof-of-Work": 3,
    "Transactions": None
  }, "0")








miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

blockchain = []
blockchain.append(first_block())

this_nodes_transactions = []

peer_nodes = []

mining = True

@node.route('/txdata', methods=['POST'])
def transaction():
  new_txion = xrequest.get_json()

  this_nodes_transactions.append(new_txion)

  print("New transaction")
  print("FROM: {}".format(new_txion['from'].encode('ascii','replace')))
  print("TO: {}".format(new_txion['to'].encode('ascii','replace')))
  print("AMOUNT: {}\n".format(new_txion['amount']))

  return "TX Data is transmitted successfully.\n"





@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain
  for i in range(len(chain_to_send)):
    block = chain_to_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    chain_to_send[i] = {
      "index": block_index,
      "timestamp": block_timestamp,
      "data": block_data,
      "hash": block_hash
    }
  chain_to_send = json.dumps(chain_to_send)
  return chain_to_send






def find_new_chains():
  other_chains = []
  for node_url in peer_nodes:
    block = requests.get(node_url + "/blocks").content
    block = json.loads(block)
    other_chains.append(block)
  return other_chains





def consensus():
  other_chains = find_new_chains()
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  blockchain = longest_chain







def proof_of_work(last_proof):
  incrementor = last_proof + 1
  while not (incrementor % 3 == 0 and incrementor % last_proof == 0):
    incrementor += 1
  return incrementor




@node.route('/mining', methods = ['GET'])
def mine():
  last_block = blockchain[len(blockchain) - 1]
  last_proof = last_block.data['Proof-of-Work']
  proof = proof_of_work(last_proof)
  this_nodes_transactions.append(
    { "From": "network", "To": miner_address, "Amount": 1 }
  )
  new_block_data = {
    "Proof-of-Work": proof,
    "Transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = this_timestamp = date.datetime.now()
  last_block_hash = last_block.hash

  this_nodes_transactions[:] = []

  mined_block = FTCBlock(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  blockchain.append(mined_block)






  return json.dumps({
      "Index": new_block_index,
      "Timestamp": str(new_block_timestamp),
      "Data": new_block_data,
      "Hash Value": last_block_hash
  }) + "\n"


node.run()


