from flask import Flask,redirect,render_template,request,session
from commandLine.blockChain import BlockChain
from commandLine.transaction import Transaction
from ellipticcurve.privateKey import PrivateKey
from argon2 import PasswordHasher

ph=PasswordHasher()
mycoin=BlockChain()
users={}
privateKeys=set()
'''
Will store key value pair of user:
    username:
    {
        privateKey:"privateKey",
        publicKey:"publicKey",
        passwordHash:(Password Hash produced by argon2)
        mineReward:int(100 by default),
        balance:500 by default
    }
'''
MAX_TRANSACTIONS=5 # maximum number of transactions to be processed in one block
app=Flask(__name__)

def generateKeypair():
    n=len(privateKeys)
    privateKey=publicKey=None
    while n==len(privateKeys):
        privateKey=PrivateKey()
        publicKey=privateKey.publicKey()
    return privateKey,publicKey
@app.route('/')
def homePage():
    if "user"in session:
        return render_template("index.html") # add arguments
    else:
        redirect("/login/")

@app.route("/login/",methods=["GET","POST"])
def  loginPage():
    if "user" in session:
        return redirect("/")
    else:
        if request.method=="POST":
            username=request.form.get("username")
            password=request.form.get("pass")
            if username in users and ph.verify(users[username]["passwordHash"],password):
                session["user"]=username
                return redirect("/")
            passwordHash=ph.hash(password)
            privateKey,publicKey=generateKeypair()
            users[username]={
                "privateKey":privateKey,
                "publicKey":publicKey,
                "passwordHash":passwordHash,
                "mineReward":100,
                "balance":500 
            }
            session["user"]=username
            return redirect("/")
        return render_template("login.html")

@app.route("/create_transaction/",methods=["GET","POST"])
def createTransaction():
    if "user" not in session:
        return redirect("/login/")
    if request.method=="POST":
        if request.form.get("sentTo")!=users[session["user"]]["privateKey"]:
            return "Transaction Not Valid"
        tx=Transaction(request.form.get("sentTo"),request.form.get("sentTo"),request.form.get("amount"))
        tx.sign()
        mycoin.addTransaction(tx)
        if len(mycoin.pendingTransactions)>=MAX_TRANSACTIONS:
            mycoin.minePendingTransactions()
    else:
        return render_template("create_ransaction.html",publicKey=users[session["user"]]["publicKey"])

@app.route("/settings/",methods=["GET","POST"])
def settingsPage():
    if "user" not in session:
        return redirect("/login/")
    if request.method=="POST":  
        users[session["user"]]["mineReward"]=request.form.get("mineReward")
        users[session["user"]]["balance"]=request.form.get("balance")%1000000        
    else:
        return render_template("settings.html",miningReward=users[session["user"]]["mineReward"],balance=users[session["user"]]["balance"])

if __name__=="__main__":
    app.run(Debug=True)