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
    def __init__(self, sentFrom:str, sentTo:str, amount:int) -> None:
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

    def __repr__(self)->str:
        return str({"sentFrom": self.sentFrom, "sentTo": self.sentTo, "amount": self.amount})
