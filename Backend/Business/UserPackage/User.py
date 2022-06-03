import django

from Backend.Business.StorePackage.Cart import Cart
from Backend.Business.Transactions.UserTransaction import UserTransaction
from Backend.Interfaces.IMarket import IMarket
import Backend.Business.Market as m
from typing import Dict
import uuid
import threading
from concurrent.futures import Future
import os

from ModelsBackend.models import CartModel, UserModel, UserTransactionModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
django.setup()

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User as m_User, Group


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

    def __init__(self, model=None):
        #  threading.Thread.__init__(self, target=t, args=args)
        # threading.Thread.__init__(self)

        # self.__id = str(uuid.uuid4())  # unique id
        # self._cart = Cart(self.__id)
        # self.__memberCheck = False
        # self.__transactions: Dict[int: UserTransaction] = {}
        self.__market: IMarket = m.Market.getInstance()
        # if model is not None:
        #     self._model = model

        self.userid = uuid.uuid4()
        self._userCart = Cart(self.userid)
        self._model = UserModel.objects.get_or_create(userid=self.userid, cart=self._userCart.getModel())[0]

        # self.start()

    # all the transaction should be access only from member !!!!
    def getTransactions(self):
        transactions: Dict[int: UserTransaction] = {}
        for model in UserTransactionModel.objects.filter(userID=self.userid):
            transaction = self._buildUserTransaction(model)
            transactions[transaction.getUserTransactionId()] = transaction
        return transactions

    def addTransaction(self, userTransaction: UserTransaction):
        pass
        # self.__transactions[userTransaction.getUserTransactionId()] = userTransaction

    def removeTransaction(self, transactionId):
        UserTransactionModel.objects.get(transactionId=transactionId).delete()

    def getTransactionById(self, transactionId):
        model = UserTransactionModel.objects.get(transactionId=transactionId)
        return self._buildUserTransaction(model)
        # return self.__transactions[transactionId]

    def getUserID(self):
        return self._model.userid

    def getCart(self):
        return Cart(model=CartModel.objects.get(userid=self._model.userid))

    def getMemberCheck(self):
        pass
        # return self.__memberCheck

    def setICart(self, icart):
        self._model.cart = icart.getModel()

    def setMemberCheck(self, state):
        pass
        # self.__memberCheck = state

    def getCartSum(self):
        try:
            return self.__market.getCartSum(self)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addProductToCart(self, storeID, product, quantity):
        try:
            return self.__market.addProductToCart(self, storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addProductToCartWithoutStore(self, product, quantity):
        try:
            return self.__market.addProductToCartWithoutStore(self, product, quantity)
        except Exception as e:
            raise Exception(e)


    @threaded
    def removeProductFromCart(self, storeID, productId):
        try:
            return self.__market.removeProductFromCart(storeID, self,  productId)
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


    @staticmethod
    def get_user(username):
        try:
            if username is None:
                model = m_User.objects.filter(username='AnonymousUser')[0]
            else:
                model = m_User.objects.get(username=username)
            return model
        except Exception as e:
            return None

    def is_authenticated(self):
        return self._model.is_authenticated

    @staticmethod
    def save(username, password):
        m_User.objects.create_user(username=username, password=password)

    @staticmethod
    def save_admin(username, password):
        m_User.objects.create_superuser(username=username, password=password)

    def getModel(self):
        return self._model

    # def __eq__(self, other):
    #     return isinstance(other, User) and self.__model == other.getModel()
    #
    # def __hash__(self):
    #     return hash(self.__model.userid)

    def _buildUserTransaction(self, model):
        return UserTransaction(model=model)


    def removeUser(self):
        self._model.delete()

