from Business.StorePackage.Cart import Cart
from Business.StorePackage.Bag import Bag
from Payment.PaymentStatus import PaymentStatus
from Payment.PaymentStatus import PaymentStatus
from Business.Transactions.UserTransaction import UserTransaction
from typing import Dict
import uuid


class User:
    def __init__(self):
        self.__id = str(uuid.uuid4())  # unique id
        self._cart = Cart(self.__id)
        self.__memberCheck = False
        self.__paymentStatus: Dict[int: PaymentStatus] = {}
        self.__transactions: Dict[int: UserTransaction] = {}

    def getPaymentStatus(self):
        return self.__paymentStatus

    def getTransactions(self):
        return self.__transactions

    def addTransaction(self, userTransaction: UserTransaction):
        self.__transactions[userTransaction.getUserTransactionId()] = userTransaction

    def removeTransaction(self, transactionId):
        self.__transactions.pop(transactionId)

    def getTransaction(self, transactionId):
        return self.__transactions[transactionId]

    def getPaymentById(self, paymentID):
        return self.__paymentStatus[paymentID]

    def addPaymentStatus(self, paymentStatus):
        self.__paymentStatus[paymentStatus.getPaymentId()] = paymentStatus

    def removePaymentStatus(self, paymentStatusId):
        self.__paymentStatus.pop(paymentStatusId)

    def getUserID(self):
        return self.__id

    def getCart(self):
        return self._cart

    def getMemberCheck(self):
        return self.__memberCheck

    def setICart(self, icart):
        self._cart = icart

    def setMemberCheck(self, state):
        self.__memberCheck = state

    def getShopingCartProducts(self):
        return self._cart.getAllProduct()

    def updateProductInCart(self, storeId, productId, quantity):
        self._cart.updateProduct(storeId, productId, quantity)

    def removeProduct(self, storeId, productId):
        self._cart.removeProduct(storeId, productId)

    def addProduct(self, storeId, product, quantity):
        self._cart.addProduct(storeId, product, quantity)

