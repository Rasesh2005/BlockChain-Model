import hashlib


class Transaction:
    """
    A Class Containing All Transaction information
    Attributes
    ----------
    amount : int
        the number of coins being transacted
    sentFrom : str
        the address of user sending amount
    sentTo : str
        the address of user receiving amount

    """

    def __init__(self, sentFrom: str, sentTo: str, amount: int) -> None:
        """
        Parameters
        ----------
        amount : int
            the number of coins being transacted
        sentFrom : str
            the address of user sending amount
        sentTo : str
            the address of user receiving amount
        ----------
        """
        self.sentFrom = sentFrom
        self.sentTo = sentTo
        self.amount = amount
        self.signature = None
        self.txHash = None

    def generateHash(self) -> str:
        return hashlib.sha256(f"{self.sentFrom}{self.sentTo}{self.amount}".encode()).hexdigest()

    def sign(self, signing_keypair:tuple):
        """
        Parameters
        ----------
        signing_keypair: tuple[2]
            contains pair of keys (private_key,public_key)
        """
        pvt_key,pub_key=signing_keypair
        if pub_key != self.sentFrom:
            raise Exception("You Cannot Sign transaction for other's wallets")
        self.txHash = self.generateHash()
        self.signature = pvt_key.sign(self.txHash.encode())

    def isValid(self, public_key):
        """
        Validates the transaction if it is signed by sender or it is a reward transaction or none of these
        Parameter
        ---------
        public_key : PublicKey
            the public key of the user's bitcoin wallet
        """
        if self.sentFrom is None:
            return True

        if not self.signature or not len(str(self.signature)):
            raise Exception("Transaction Not Signed")

        valid = public_key.verify(self.signature, self.txHash.encode())
        return valid

    def __repr__(self) -> str:
        return str({"sentFrom": self.sentFrom, "sentTo": self.sentTo, "amount": self.amount})
