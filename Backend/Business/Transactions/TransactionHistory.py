from Backend.Business.Transactions.StoreTransaction import StoreTransaction
from Backend.Business.Transactions.UserTransaction import UserTransaction
from typing import Dict


class TransactionHistory:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TransactionHistory.__instance is None:
            TransactionHistory()
        return TransactionHistory.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__storeTransactions: Dict[int: StoreTransaction] = {}
        self.__userTransaction: Dict[int: UserTransaction] = {}
        if TransactionHistory.__instance is None:
            TransactionHistory.__instance = self

    def addStoreTransaction(self, st):
        if st.getTransactionID() in self.__storeTransactions.keys():
            raise Exception("transaction with Id: " + str(st.getTransactionID()) + "is all ready exists")
        self.__storeTransactions[st.getTransactionID()] = self.__createStoreTransaction(st)

    def addUserTransaction(self, ut):
        if ut.getUserTransactionId() in self.__userTransaction.keys():
            raise Exception("transaction with Id: " + str(ut.getUserTransactionId()) + "is all ready exists")
        self.__userTransaction[ut.getUserTransactionId()] = self.__createUserTransaction(ut)

    def getAllStoreTransactions(self):
        return self.__storeTransactions.values()

    def getAllUserTransactions(self):
        return self.__userTransaction.values()

    def getStoreTransaction(self, transactionId):
        if transactionId in self.__storeTransactions.keys():
            raise Exception("transaction with Id: " + str(transactionId) + "is all ready exists")
        return self.__storeTransactions.get(transactionId)

    def getUserTransaction(self, transactionId):
        if transactionId in self.__userTransaction.keys():
            raise Exception("transaction with Id: " + str(transactionId) + "is all ready exists")
        return self.__userTransaction.get(transactionId)

    def getStoreTransactionById(self, transactionId):
        transaction = self.__storeTransactions.get(transactionId)
        if transaction is None:
            raise Exception("transaction with Id: " + str(transactionId) + "doesn't exists")
        return transaction

    def getUserTransactionById(self, transactionId):
        transaction = self.__userTransaction.get(transactionId)
        if transaction is None:
            raise Exception("transaction with Id: " + str(transactionId) + "doesn't exists")
        return transaction

    def __createStoreTransaction(self, st):
        return StoreTransaction(st.getStoreId(), st.getStoreName(), st.getTransactionID(),
                                st.getPaymentId(), st.getProducts(), st.getAmount())

    def __createUserTransaction(self, ut):
        return UserTransaction(ut.getUserId(), ut.getUserTransactionId(), ut.getStoreTransactions(), ut.getPaymentId(),
                               ut.getTotalAmount())
