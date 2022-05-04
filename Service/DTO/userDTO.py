from Service.DTO import cartDTO,paymentStatusDTO,userTransactionDTO
from typing import Dict

class userDTO:
    def __init__(self):
        self.__id = id  # unique id
        self.__memberCheck = False
        self.__paymentStatus: Dict[int: paymentStatusDTO] = {}
        self.__transactions: Dict[int: userTransactionDTO] = {}
        self.__cart: cartDTO = cart

    def getPaymentStatus(self):
        return self.__paymentStatus

    def getTransactions(self):
        return self.__transactions

    def getUserID(self):
        return self.__id

    def getCart(self):
        return self.__cart

    def getMemberCheck(self):
        return self.__memberCheck

    def setICart(self, cart):
        self.__cart = cart

    def setMemberCheck(self, state):
        self.__memberCheck = state

    def setUserID(self,uid):
        self.__id=uid

    def setPaymentStatus(self,status : paymentStatusDTO):
        self.__paymentStatus = paymentStatusDTO

    def setTransactions(self, transaction : Dict[int: userTransactionDTO]):
        self.__transactions = transaction




