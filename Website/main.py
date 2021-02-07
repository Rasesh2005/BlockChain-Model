from ecdsa.keys import VerifyingKey
from flask import Flask,redirect,render_template,request,session
from ecdsa import SigningKey
from argon2 import PasswordHasher

from components.blockChain import BlockChain
from components.transaction import Transaction

ph=PasswordHasher()
mycoin=BlockChain()
users={}
publicKeys=set()
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
MAX_TRANSACTIONS=1 # maximum number of transactions to be processed in one block
app=Flask(__name__)
app.secret_key="VerySecretKey"


def to_string(key,isPublic):
    if isPublic:
        return key.to_pem()[len(b"-----BEGIN PUBLIC KEY-----\n"):-len(b"\n-----END PUBLIC KEY-----\n")].decode()
    return key.to_pem()[len(b"-----BEGIN EC PRIVATE KEY-----\n"):-len(b"\n-----END EC PRIVATE KEY-----\n")].decode()


def to_pem(key_str,isPublic):
    if isPublic:
        return b"-----BEGIN PUBLIC KEY-----\n"+key_str.encode()+b"\n-----END PUBLIC KEY-----\n"
    return b"-----BEGIN EC PRIVATE KEY-----\n"+key_str.encode()+b"\n-----END EC PRIVATE KEY-----\n"

def remove_escapeChar(word):
    res=""
    for i in word:
        if i not in ['\n','\t','\r','\b']:
            res+=i

    return res
def generateKeypair():
    print("Generating Key")
    n=len(publicKeys)
    privateKey=publicKey=None
    while n==len(publicKeys):
        privateKey=SigningKey.generate()
        publicKey=privateKey.verifying_key
        publicKeys.add(to_string(publicKey,True))
    return privateKey,publicKey
@app.route('/')
def homePage():
    if "user"in session:
        return render_template("index.html",blocks=mycoin.chain,balance=mycoin.getBalanceOfAddress(remove_escapeChar(to_string(users[session["user"]]["publicKey"],True)),users[session["user"]]["balance"]))# add arguments
    else:
        return redirect("/login/")

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
        sendFrom=remove_escapeChar(to_string(users[session["user"]]["publicKey"],True))
        if request.form.get("sendFrom")!=sendFrom:
            return "Transaction Not Valid"
        try:
            tx=Transaction(request.form.get("sendFrom"),request.form.get("sendTo"),int(request.form.get("amount")))
            tx.sign((users[session["user"]]["privateKey"],users[session["user"]]["publicKey"]))
            mycoin.addTransaction(tx,users[session["user"]]["publicKey"])
        except:
            return redirect('/create_transaction/')
        if len(mycoin.pendingTransactions)>=MAX_TRANSACTIONS:
            mycoin.minePendingTransactions(users[session["user"]]["publicKey"])
        return redirect("/")
    else:
        return render_template("create_transaction.html",publicKey=to_string(users[session["user"]]["publicKey"],True),balance=mycoin.getBalanceOfAddress(remove_escapeChar(to_string(users[session["user"]]["publicKey"],True)),users[session["user"]]["balance"]))

@app.route("/settings/",methods=["GET","POST"])
def settingsPage():
    balance=mycoin.getBalanceOfAddress(remove_escapeChar(to_string(users[session["user"]]["publicKey"],True)),users[session["user"]]["balance"])
    if "user" not in session:
        return redirect("/login/")
    if request.method=="POST":  
        users[session["user"]]["mineReward"]=request.form.get("mineReward")
        users[session["user"]]["balance"]+=int(request.form.get("balance")) 
        return render_template("settings.html",miningReward=users[session["user"]]["mineReward"],balance=users[session["user"]]["balance"],success=True)
    return render_template("settings.html",miningReward=users[session["user"]]["mineReward"],balance=balance)

if __name__=="__main__":
    app.run(threaded=True)