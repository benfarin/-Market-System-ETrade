from typing import Dict
from Service.DTO import storeTransactionDTO,paymentStatusDTO


class userTransactionDTO:
    def __init__(self, userID, transactionId, storeTransactions, paymentsStatus):
        self.__userID = userID
        self.__transactionId = transactionId
        self.__storeTransactions: Dict[int: storeTransactionDTO] = storeTransactions
        self.__paymentStatus : paymentStatusDTO = paymentsStatus

    def getUserTransactionId(self):
        return self.__transactionId

    def getStoreTransactions(self):
        return self.__storeTransactions

    def getPaymentStatus(self):
        return self.__paymentStatus

    def getUserID(self):
        return self.__userID

    def setUserTransactionId(self,id):
        self.__transactionId = id

    def setStoreTransactions(self, transaction: Dict[int: storeTransactionDTO]):
        self.__storeTransactions = transaction

    def setPaymentStatus(self, status):
        self.__paymentStatus = status

    def setUserID(self, userid):
        __userID = userid