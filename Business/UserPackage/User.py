from Business.StorePackage.Cart import Cart
from Business.StorePackage.Bag import Bag
from Payment.PaymentStatus import PaymentStatus
from Payment.PaymentStatus import PaymentStatus
from Business.Transactions.UserTransaction import UserTransaction
from typing import Dict
import uuid
import threading
from concurrent.futures import Future


def call_with_future(fn, future, args, kwargs):
    try:
        result = fn(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)


def threaded(fn):
    def wrapper(*args, **kwargs):
        future = Future()
        threading.Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future.result()

    return wrapper


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

    @threaded
    def addTransaction(self, userTransaction: UserTransaction):
        self.__transactions[userTransaction.getUserTransactionId()] = userTransaction

    @threaded
    def removeTransaction(self, transactionId):
        self.__transactions.pop(transactionId)

    def getTransaction(self, transactionId):
        return self.__transactions[transactionId]

    def getPaymentById(self, paymentID):
        return self.__paymentStatus[paymentID]

    @threaded
    def addPaymentStatus(self, paymentStatus):
        self.__paymentStatus[paymentStatus.getPaymentId()] = paymentStatus

    @threaded
    def removePaymentStatus(self, paymentStatusId):
        self.__paymentStatus.pop(paymentStatusId)

    def getUserID(self):
        return self.__id

    def getCart(self):
        return self._cart

    def getMemberCheck(self):
        return self.__memberCheck

    @threaded
    def setICart(self, icart):
        self._cart = icart

    @threaded
    def setMemberCheck(self, state):
        self.__memberCheck = state

    def getShopingCartProducts(self):
        return self._cart.getAllProduct()

    @threaded
    def updateProductInCart(self, storeId, productId, quantity):
        self._cart.updateProduct(storeId, productId, quantity)

    @threaded
    def removeProduct(self, storeId, productId):
        self._cart.removeProduct(storeId, productId)

    @threaded
    def addProduct(self, storeId, product, quantity):
        self._cart.addProduct(storeId, product, quantity)
