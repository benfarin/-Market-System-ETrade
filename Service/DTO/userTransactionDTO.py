from typing import Dict

from Business.Transactions import StoreTransaction
from Service.DTO.StoreTransactionForUserDTO import storeTransactionForUserDTO
from Business.Transactions.UserTransaction import UserTransaction


class userTransactionDTO:
    def __init__(self, userTransaction: UserTransaction):
        self.__userID = userTransaction.getUserId()
        self.__transactionId = userTransaction.getUserTransactionId()
        self.__storeTransactions: Dict[int: storeTransactionForUserDTO] = self.__makeDtoTransaction(userTransaction.getStoreTransactions())
        self.__paymentId = userTransaction.getPaymentId()

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

    def __makeDtoTransaction(self, storeTransactions: {int: StoreTransaction}):
        transactionList = {}
        for st in storeTransactions.values():
            transactionList[st.getStoreId()] = storeTransactionForUserDTO(st)
        return transactionList
