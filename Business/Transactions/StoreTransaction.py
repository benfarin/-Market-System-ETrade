from Business.Transactions.Transaction import Transaction
from typing import Dict

class StoreTransaction:

    def __init__(self, storeId, storeName):
        self.__storeId = storeId
        self.__storeName = storeName
        self.__transactions: Dict[int: Transaction] = {}

    def addTransaction(self, transaction):
        self.__transactions[transaction.getTransactionID()] = transaction

    def removeTransaction(self, transactionId):
        if transactionId not in self.__transactions.keys():
            raise Exception("cannot remove transaction with wrong transactionId")
        self.__transactions.pop(transactionId)

    def getTransactionHistory(self):
        return self.__transactions

    def getPurchaseHistoryInformation(self):
        info = "purchase history for store: " + self.__storeName + " ,storeId: " + str(self.__storeId) + " :\n"
        for transaction in self.__transactions:
            info += transaction.__str__() + "\n"
        return info

