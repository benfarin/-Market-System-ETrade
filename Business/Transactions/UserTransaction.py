from Business.Transactions.Transaction import Transaction
from typing import Dict
class UserTransaction:
    def __init__(self,userID):
        self.__userID = userID
        self.__transactions : [Transaction] = []


    def addUserTransaction(self,transaction):
        if self.__transactions.append(transaction):
            return True
        else:
            return False

    def updateUserTransaction(self,transactionID, updatedTransaction):
        try:
            trans: Transaction = None
            for trans in (self.__transactions):
                if trans.getTransactionID() == transactionID:
                    self.__transactions.remove(trans)
                    self.__transactions.append(updatedTransaction)
                else:
                    raise Exception("This transaction ID " + transactionID + " does not exist!")
        except Exception as e:
            return e
    def removeUserTransaction(self,transactionID):
        try:
            trans: Transaction = None
            for trans in (self.__transactions):
                if trans.getTransactionID() == transactionID:
                    self.__transactions.remove(transactionID)
                else:
                    raise Exception("This transaction ID "+ transactionID +" does not exist!")
        except Exception as e:
            return e