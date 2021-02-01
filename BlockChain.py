from Block import Block
from Transaction import Transaction
class BlockChain:
    def __init__(self) -> None:
        self.pendingTransactions=[]
        self.chain=[self.createGenesisBlock()]     
        self.difficulty=2
        # Miners Get coins on mining a new block...
        self.miningReward=100

    def createGenesisBlock(self):
        return Block(self.pendingTransactions,"0000")


    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]

    def minePendingTransactions(self,miningRewardAddress):
        block=Block(transactions=self.pendingTransactions,previousHash=self.getLatestBlock().hash)
        block.mineBlock(self.difficulty)

        print(f"Block Successfully mined by user {miningRewardAddress}")
        self.chain.append(block)

        self.pendingTransactions=[
            Transaction(None,miningRewardAddress,self.miningReward)
        ]
    def createTransaction(self,transaction):
        self.pendingTransactions.append(transaction)


    def getBalanceOfAddress(self,address):
        balance=0

        for block in self.chain:
            for t in block.transactions:
                if t.sentFrom==address:
                    balance-=t.amount
                if t.sentTo==address:
                    balance+=t.amount
        return balance
        
    
    ## Adding A Block Without Reward
    # def addBlock(self,newBlock):
    #     newBlock.previousHash=self.getLatestBlock().hash
    #     newBlock.mineBlock(self.difficulty)
    #     self.chain.append(newBlock)
    def checkValidity(self):
        for i in range(1,len(self.chain)):
            currentBlock=self.chain[i]
            prevBlock=self.chain[i-1]
            if currentBlock.hash!=currentBlock.generateHash():
                return False
            if currentBlock.previousHash!=prevBlock.hash:
                return False
        return True
    def __repr__(self) -> str:
        return str({"BlockChain":{i:item for i,item in enumerate(self.chain)}})