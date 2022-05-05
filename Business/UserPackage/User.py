from Business.StorePackage.Cart import Cart
from Payment.PaymentStatus import PaymentStatus
from Business.Transactions.UserTransaction import UserTransaction
from interfaces.IMarket import IMarket
from Business.Market import Market
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


# class User(threading.Thread):
class User:

    def __init__(self):
        #  threading.Thread.__init__(self, target=t, args=args)
        # threading.Thread.__init__(self)

        self.__id = str(uuid.uuid4())  # unique id
        self._cart = Cart(self.__id)
        self.__memberCheck = False
        self.__paymentStatus: Dict[int: PaymentStatus] = {}
        self.__transactions: Dict[int: UserTransaction] = {}
        self.__market: IMarket = Market.getInstance()
        # self.start()

    def getPaymentStatus(self):
        return self.__paymentStatus

    # all the transaction should be access only from member !!!!
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

    @threaded
    def addProductToCart(self, storeID, product, quantity):
        try:
            return self.__market.addProductToCart(self, storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    @threaded
    def removeProductFromCart(self, storeID, productId):
        try:
            return self.__market.removeProductFromCart(self, storeID, productId)
        except Exception as e:
            raise Exception(e)

    @threaded
    def updateProductFromCart(self, storeID, productId, quantity):
        try:
            return self.__market.addProductToCart(self, storeID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    @threaded
    def purchaseCart(self, bank):
        try:
            return self.__market.purchaseCart(self, bank)
        except Exception as e:
            raise Exception(e)


