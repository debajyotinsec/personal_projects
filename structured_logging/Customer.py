from CustBasic import *
from CustAddress import *
from CustCard import *
import json

class Customer():
    def __init__(self):
        self.cust_basic: CustBasic = CustBasic()
        self.cust_address: list[CustAddress] = list()
        self.cust_card: list[CustCard] = list()

    def __str__(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=2)


    