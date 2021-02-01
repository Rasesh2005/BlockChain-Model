import hashlib
import time

class Block:
    def __init__(self,transactions,previousHash=""):
        self.t=time.localtime()
        self.previousHash=previousHash
        self.timeStamp=f"{self.t.tm_mday}/{self.t.tm_mon}/{self.t.tm_year} {self.t.tm_hour}:{self.t.tm_min}:{self.t.tm_sec}"
        self.transactions=transactions

        # Nonce is used to try different String hashes so that the hash ends with desired value..
        self.nonce=0

        self.hash=self.generateHash()
    def generateHash(self):
        return hashlib.sha256(f"{self.previousHash}{self.timeStamp}{self.transactions}{self.nonce}".encode()).hexdigest()

    # Proof Of Work Or Mining Block of BlockChain
    def mineBlock(self,difficulty):
        while self.hash[:difficulty]!="0"*difficulty:
            self.nonce+=1
            self.hash=self.generateHash()
        # print(f"Hash Found={self.hash}")

    
    def __repr__(self) -> str:
        return str({"timestamp":self.timeStamp,"transactions":self.transactions,"previousHash":self.previousHash,"hash":self.hash})