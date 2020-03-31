import hashlib
import datetime
import time
import json

INITIAL_BITS = 0x1e777777
MAX_32BIT    = 0xffffffff

class Block():
    def __init__(self,index,prev_hash,data,timestamp,bits):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp
        self.bits = bits # difficulty bits
        self.nonce = 0
        self.elapsed_time = ''
        self.block_hash = ''

    def __str__(self):
        return json.dumps(self.to_json(), indent=2, sort_keys = True, ensure_ascii = False)
    __repr__ = __str__

    def __setitem__(self,key,value):
        setattr(self,key,value) # self.key = value

    def to_json(self):
        res = {
                'index': self.index,
                'prev_hash' : self.prev_hash,
                'stored_data' : self.data,
                'timestamp' : self.timestamp.strftime('%Y/%M/%d %H:%M:%S'),
                'bits' : hex(self.bits)[2:].rjust(8,'0'),
                'nonce' : self.nonce,
                'elapsed_time' : self.elapsed_time,
                'block_hash' : self.blcok_hash
                }
        return res

    def calc_blockhash(self):
        blockheader = str(self.index) + str(self.prev_hash) + str(self.data) + str(self.timestamp) + hex(self.bits)[2:] + str(self.nonce)
        h = hashlib.sha256(blockheader.encode()).hexdigest()
        self.blcok_hash = h
        return h

    def calc_target(self):
        exponent_bytes = (self.bits >> 24) -3 # the former 1 bytes of difficulty bits
        exponent_bits  = exponent_bytes * 8
        coefficient = self.bits & 0xffffff # the latter 3 bytes of difficulty bits
        return coefficient << exponent_bits

    def chech_valid_hash(self):
        return int(self.calc_blockhash(),16) <= self.calc_target()

class BlockChain():
    def __init__(self,initial_bits):
        self.chain = []
        self.initial_bits = initial_bits

    def add_block(self,block):
        self.chain.append(block)

    def get_block_info(self,index=-1):
        print(json.dumps(self.chain[index].to_json(), indent=2, sort_keys = True, ensure_ascii = False))
        return

    def mining(self,block):
        start_time = int(time.time() * 1000)
        while 1:
            for n in range(MAX_32BIT + 1):
                block.nonce = n
                if block.chech_valid_hash():
                    end_time = int(time.time() * 1000)
                    block.elapsed_time = str((end_time - start_time) / 1000.0) + 's'
                    self.add_block(block)
                    self.get_block_info()
                    return
            new_time = datetime.datetime.now()
            if new_time == block.timestamp:
                block.timestamp += datetime.timedelta(seconds = 1)
            else:
                block.timestamp = new_time

    def create_genesis(self):
        genesis_block = Block(0,'0'*32*2,'Genesis Block',datetime.datetime.now(),self.initial_bits)
        self.mining(genesis_block)

    def add_new_block(self,i):
        last_block = self.chain[-1]
        block = Block(i+1, last_block.block_hash, 'block '+str(i+1), datetime.datetime.now(), last_block.bits)
        self.mining(block)
