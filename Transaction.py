class Transaction:
    def __init__(self,sentFrom,sentTo,amount) -> None:
        super().__init__()
        self.sentFrom=sentFrom
        self.sentTo=sentTo
        self.amount=amount
    
    def __repr__(self):
        return str({"sentFrom":self.sentFrom,"sentTo":self.sentTo,"amount":self.amount})
