from Business.Transactions.StoreTransaction import StoreTransaction
from typing import Dict


class UserTransaction:
    def __init__(self, userID, transactionId, storeTransactions, paymentsStatus):
        self.__userID = userID
        self.__transactionId = transactionId
        self.__storeTransactions: Dict[int: StoreTransaction] = storeTransactions
        self.__paymentStatus = paymentsStatus

    def getUserTransactionId(self):
        return self.__transactionId

    def getStoreTransactions(self):
        return self.__storeTransactions

    def getPaymentStatus(self):
        return self.__paymentStatus

