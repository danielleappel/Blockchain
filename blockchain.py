# Using https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/
# as a resources

from hashlib import sha256
import json
from time import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash=None, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time(), "0")
        genesis_block.hash = genesis_block.hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    difficulty = 2
    def proof_of_work(self, block):
        computed_hash = block.hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            print(computed_hash, "\n")
            block.nonce += 1
            computed_hash = block.hash()
        return computed_hash

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)
    
    def mine(self):
        if not self.unconfirmed_transactions:
            return False
    
        last_block = self.last_block
    
        new_block = Block(index=last_block.index + 1,
                        transactions=self.unconfirmed_transactions,
                        timestamp=time(),
                        previous_hash=last_block.hash)
    
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

def main():
    b = Block(2,4,"10:02",145632)
    print(b.hash())
    print(b.nonce)
    bc = Blockchain()
    print(bc.add_block(b, bc.proof_of_work(b)))
    print(bc.mine())
    print(bc.chain)
    print(b.nonce)

if __name__ == "__main__":
    main()
    
