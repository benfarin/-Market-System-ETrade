
from Business.Transactions.Transaction import Transaction
from typing import Dict


class UserTransaction:
    def __init__(self, userID):
        self.__userID = userID
        self.__transactions: Dict[int: Transaction] = {}

    def addTransaction(self, transaction):
        self.__transactions[transaction.getTransactionID()] = transaction

    def removeTransaction(self, transactionId):
        if transactionId not in self.__transactions.keys():
            raise Exception("cannot remove transaction with wrong transactionId")
        self.__transactions.pop(transactionId)

    def getTransactionHistory(self):
        return self.__transactions
