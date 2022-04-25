from Business.StorePackage.Cart import Cart
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
        self.__transactions = UserTransaction(self.__id)

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

    def userPurchaseCart(self, bank, phone, address):  # bank - Bank , phone - string , address ->Address
        pass

    def updateProductInCart(self, storeId, productId, quantity):
        self._cart.updateProduct(storeId, productId, quantity)

    def removeProduct(self, storeId, productId):
        self._cart.removeProduct(storeId, productId)

    def addProduct(self, storeId, product, quantity):
        self._cart.addProduct(storeId, product, quantity)

    def addPaymentStatus(self, paymentStatus):
        #need to add cancel
        self.__paymentStatus[paymentStatus.getPaymentId()] = paymentStatus

    def addTransaction(self, transaction):
        return self.__transactions.addTransaction(transaction)

    def removeTransaction(self, transactionId):
        try:
            return self.__transactions.removeTransaction(transactionId)
        except Exception as e:
            raise Exception(e)



