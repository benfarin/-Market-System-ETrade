from Backend.Business.Transactions.StoreTransaction import StoreTransaction
from typing import Dict
from ModelsBackend.models import UserTransactionModel, StoreTransactionsInUserTransactions
import datetime


class UserTransaction:
    def __init__(self, userID, transactionId, storeTransactions, paymentId, totalAmount):
        # self.__userID = userID
        # self.__transactionId = transactionId
        # self.__paymentId = paymentId
        # self.__date = datetime.datetime.now().strftime("%x") + " " + datetime.datetime.now().strftime("%X")
        # self.__storeTransactions: Dict[int: StoreTransaction] = storeTransactions
        # self.__totalAmount = totalAmount
        self.__ut = UserTransactionModel(userID=userID, transactionId=transactionId, paymentId=paymentId,
                                         date=datetime.datetime.now(), totalAmount=totalAmount)
        self.__ut.save()
        for st in storeTransactions:
            StoreTransactionsInUserTransactions(userTransaction_id=self.__ut,
                                                storeTransaction_id=st.getModel()).save()

    def getUserId(self):
        return self.__ut.userID

    def getUserTransactionId(self):
        return self.__ut.transactionId

    def getStoreTransactions(self):
        return [StoreTransaction(model=stiut.storeTransaction_id)
                for stiut in StoreTransactionsInUserTransactions.objects.filter(userTransaction_id=self.__ut.transactionId)]

    def getPaymentId(self):
        return self.__ut.paymentId

    def getDate(self):
        return self.__ut.date

    def getTotalAmount(self):
        return self.__ut.totalAmount

    def getModel(self):
        return self.__ut

    def removeUserTransaction(self):
        for STinUT in StoreTransactionsInUserTransactions.objects.filter(userTransaction_id=self.__ut.transactionId):
            STinUT.delete()
        self.__ut.delete()

    def __eq__(self, other):
        return isinstance(other, UserTransaction) and self.__ut == other.getModel()

    def __hash__(self):
        return hash(self.__ut.transactionId)
