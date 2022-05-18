from Backend.Business.Transactions.StoreTransaction import StoreTransaction
from typing import Dict
import datetime


class UserTransaction:
    def __init__(self, userID, transactionId, storeTransactions, paymentId, totalAmount):
        self.__userID = userID
        self.__transactionId = transactionId
        self.__paymentId = paymentId
        self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        self.__storeTransactions: Dict[int: StoreTransaction] = storeTransactions
        self.__totalAmount = totalAmount

    def getUserId(self):
        return self.__userID

    def getUserTransactionId(self):
        return self.__transactionId

    def getStoreTransactions(self):
        return self.__storeTransactions

    def getPaymentId(self):
        return self.__paymentId

    def getDate(self):
        return self.__date

    def getTotalAmount(self):
        return self.__totalAmount
