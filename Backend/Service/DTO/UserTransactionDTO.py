from typing import Dict

from Backend.Business.Transactions import StoreTransaction
from Backend.Service.DTO.StoreTransactionForUserDTO import storeTransactionForUserDTO
from Backend.Business.Transactions.UserTransaction import UserTransaction


class userTransactionDTO:
    def __init__(self, userTransaction: UserTransaction):
        self.__userID = userTransaction.getUserId()
        self.__transactionId = userTransaction.getUserTransactionId()
        self.__paymentId = userTransaction.getPaymentId()
        self.__date = userTransaction.getDate()
        self.__storeTransactions: Dict[int: storeTransactionForUserDTO] = self.__makeDtoTransaction(
            userTransaction.getStoreTransactions())
        self.__totalAmount = userTransaction.getTotalAmount()

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

    def getDate(self):
        return self.__date

    def getTotalAmount(self):
        return self.__totalAmount

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

    def __str__(self):
        toReturn = "user transaction of user: " + str(self.__userID) + ":"
        toReturn += "\n\ttransaction id: " + str(self.__transactionId)
        toReturn += "\n\tpayment id: " + str(self.__paymentId)
        toReturn += "\n\tdate: " + str(self.__date)
        toReturn += "\n\tstore transactions: "
        for st in self.__storeTransactions.values():
            toReturn += "\n\t" + st.__str__()
        return toReturn + "\n\ttotal amount: " + str(self.__totalAmount)

    def printUserTransactionWithSpace(self):
        toReturn = "\tuser transaction of user: " + str(self.__userID) + ":"
        toReturn += "\n\t\ttransaction id: " + str(self.__transactionId)
        toReturn += "\n\t\tpayment id: " + str(self.__paymentId)
        toReturn += "\n\t\tdate: " + str(self.__date)
        toReturn += "\n\t\tstore transactions: "
        for st in self.__storeTransactions.values():
            toReturn += "\n\t\t" + st.__str__()
        return toReturn + "\n\t\ttotal amount: " + str(self.__totalAmount)
