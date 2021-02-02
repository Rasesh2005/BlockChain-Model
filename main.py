from Block import Block
from BlockChain import BlockChain
from Transaction import Transaction

# Creating a BlockChain
bitcoin=BlockChain()

'''
Making A Block and mining It
'''
block=Block([Transaction("Rasesh","Uday","5")])
print("Mining Block 1")
bitcoin.addBlock(block)
block=Block([Transaction("Uday","Rasesh","5")])
print("Mining Block 2")
bitcoin.addBlock(block)

## Trying To Change Information On BlockChain
# if len(bitcoin.chain[1].transactions):
# bitcoin.chain[1].transactions[0].amount=100

# Even If We Recalculate its hash we will need to correct all further hashes or next blocks...
# bitcoin.chain[1].hash=bitcoin.chain[1].generateHash()



# If Data is tampered return False
print(bitcoin.checkValidity())


print(bitcoin)

# bitcoin.createTransaction(Transaction('add1','add2',100))
# bitcoin.createTransaction(Transaction('add2','add1',200))


# print("Mining Pending Transactions")
# # address rasesh starts mining to get reward of 100 bitcoin
# bitcoin.minePendingTransactions("rasesh")
# # add1 will mine transactions which contains the reward transaction of rasesh
# bitcoin.minePendingTransactions("add1")

# print("Balance Of User rasesh:",bitcoin.getBalanceOfAddress("rasesh"))