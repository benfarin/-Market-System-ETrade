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

from ModelsBackend.models import CartModel, UserModel

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
        # self.__market: IMarket = m.Market.getInstance()
        # if model is not None:
        #     self._model = model

        userid = uuid.uuid4()
        userCart = Cart(userid)
        self.__model = UserModel.objects.get_or_create(userid=userid, cart=userCart.getModel())[0]

        # self.start()

    # all the transaction should be access only from member !!!!
    def getTransactions(self):
        return self.__transactions

    def addTransaction(self, userTransaction: UserTransaction):
        self.__transactions[userTransaction.getUserTransactionId()] = userTransaction

    def removeTransaction(self, transactionId):
        self.__transactions.pop(transactionId)

    def getTransactionById(self, transactionId):
        return self.__transactions[transactionId]

    def getUserID(self):
        return self.__model.userid

    def getCart(self):
        return Cart(model=CartModel.objects.get(userid=self.__model.userid))

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


    @property
    def pk(self):
        return self.__id

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
        return self.__model.is_authenticated

    @staticmethod
    def save(username, password):
        m_User.objects.create_user(username=username, password=password)

    @staticmethod
    def save_admin(username, password):
        m_User.objects.create_superuser(username=username, password=password)

    def getModel(self):
        return self.__model

    # def __eq__(self, other):
    #     return isinstance(other, User) and self.__model == other.getModel()
    #
    # def __hash__(self):
    #     return hash(self.__model.userid)

