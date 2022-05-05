from typing import Dict
from Service.DTO.StoreTransactionForUserDTO import storeTransactionForUserDTO


class userTransactionDTO:
    def __init__(self, userID, transactionId, storeTransactions, paymentId):
        self.__userID = userID
        self.__transactionId = transactionId
        self.__storeTransactions: Dict[int: storeTransactionForUserDTO] = storeTransactions
        self.__paymentId = paymentId

    def getStoreTransaction(self, id):
        return self.__storeTransactions.get(id)

    def getUserTransactionId(self):
        return self.__transactionId

    def getStoreTransactions(self):
        return self.__storeTransactions

    def getPaymentId(self):
        return self.__paymentId

    def getUserID(self):
        return self.__userID

    def setUserTransactionId(self, id):
        self.__transactionId = id

    def setStoreTransactions(self, transaction):
        self.__storeTransactions = transaction

    def setPaymentId(self, paymentId):
        self.__paymentId = paymentId

    def setUserID(self, userid):
        __userID = userid
