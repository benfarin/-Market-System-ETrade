from Business.UserPackage.User import User
import bcrypt
import threading

from Exceptions.CustomExceptions import NoSuchMemberException
from interfaces.IMarket import IMarket
from Business.Market import Market
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


class Member(User):
    def __init__(self, userName, password, phone, address, bank):
        super().__init__()  # extend the constructor of user class
        self.__isLoggedIn = False
        self.__userName = userName  # string
        self.__password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # string
        self.__phone = phone  # string
        self.__address = address  # type address class
        self.__bank = bank  # type bank
        self.__market: IMarket = Market.getInstance()

    def setLoggedIn(self, state):
        self.__isLoggedIn = state

    def addProductRating(self, productID, rating):
        pass

    def getPassword(self):
        return self.__password

    def getPhone(self):
        return self.__phone

    def getBank(self):
        return self.__bank

    def getMemberName(self):
        return self.__userName

    def loginUpdates(self):
        try:
            return self.__market.loginUpdates(self)
        except Exception as e:
            raise Exception(e)

    @threaded
    def createStore(self, storeName, bank, address):
        try:
            return self.__market.createStore(storeName, self, bank, address)
        except Exception as e:
            raise Exception(e)

    @threaded
    def removeStore(self, storeId, user):
        try:
            return self.__market.removeStore(storeId, user)
        except Exception as e:
            raise Exception(e)

    @threaded
    def appointManagerToStore(self, storeID, assignee):
        try:
            return self.__market.appointManagerToStore(storeID, self, assignee)
        except Exception as e:
            raise Exception(e)

    @threaded
    def appointOwnerToStore(self, storeID, assignee):
        try:
            return self.__market.appointOwnerToStore(storeID, self, assignee)
        except Exception as e:
            raise Exception(e)

    @threaded
    def setStockManagerPermission(self, storeID, assignee):
        try:
            return self.__market.setStockManagerPermission(storeID, self, assignee)
        except Exception as e:
            raise Exception(e)

    @threaded
    def setAppointOwnerPermission(self, storeID, assignee):
        try:
            return self.__market.setAppointOwnerPermission(storeID, self, assignee)
        except Exception as e:
            raise Exception(e)

    @threaded
    def setChangePermission(self, storeID, assignee):
        try:
            return self.__market.setChangePermission(storeID, self, assignee)
        except Exception as e:
            raise Exception(e)

    @threaded
    def setRolesInformationPermission(self, storeID, assignee):
        try:
            return self.__market.setRolesInformationPermission(storeID, self, assignee)
        except Exception as e:
            raise Exception(e)

    @threaded
    def setPurchaseHistoryInformationPermission(self, storeID, assignee):
        try:
            return self.__market.setPurchaseHistoryInformationPermission(storeID, self, assignee)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addProductToStore(self, storeID, product):
        try:
            return self.__market.addProductToStore(storeID, self, product)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addProductQuantityToStore(self, storeID, productId, quantity):
        try:
            return self.__market.addProductQuantityToStore(storeID, self, productId, quantity)
        except Exception as e:
            raise Exception(e)

    @threaded
    def removeProductFromStore(self, storeID, product):
        try:
            return self.__market.removeProductFromStore(storeID, self, product)
        except Exception as e:
            raise Exception(e)

    @threaded
    def updateProductPrice(self, storeID, productId, newPrice):
        try:
            return self.__market.updateProductPrice(storeID, self, productId, newPrice)
        except Exception as e:
            raise Exception(e)

    @threaded
    def updateProductName(self, storeID, productID, newName):
        try:
            return self.__market.updateProductName(storeID, self, productID, newName)
        except Exception as e:
            raise Exception(e)

    @threaded
    def updateProductCategory(self, storeID, productID, newCategory):
        try:
            return self.__market.updateProductName(storeID, self, productID, newCategory)
        except Exception as e:
            raise Exception(e)

    @threaded
    def PrintRolesInformation(self, storeID):
        try:
            return self.__market.printRolesInformation(storeID, self)
        except Exception as e:
            raise Exception(e)

    @threaded
    def printPurchaseHistoryInformation(self, storeID):
        try:
            return self.__market.printPurchaseHistoryInformation(storeID, self)
        except Exception as e:
            raise Exception(e)
