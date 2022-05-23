from Backend.Business.UserPackage.User import User
import bcrypt
import threading

from Backend.Exceptions.CustomExceptions import NoSuchMemberException, PasswordException
from Backend.Interfaces.IMarket import IMarket
from Backend.Business.Market import Market
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
        try:
            return future.result()
        except:
            raise future.exception()

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

    def getAddress(self):
        return self.__address

    def getBank(self):
        return self.__bank

    def getMemberName(self):
        return self.__userName

    def getMemberTransactions(self):
        return super().getTransactions().values()

    def setCart(self, cart):
        self._cart = cart

    def updateCart(self, cart):
        self.__market.updateCart(self._cart, cart)

    def isStoreExists(self, storeId):
        return self.__market.isStoreExists(storeId)

    def loginUpdates(self):
        try:
            return self.__market.loginUpdates(self)
        except Exception as e:
            raise Exception(e)

    def change_password(self, old_password, new_password):
        if bcrypt.checkpw(old_password.encode('utf-8'), self.__password):
            self.__password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            return "Password changed succesfully!"
        else:
            raise PasswordException("password not good!")

    @threaded
    def createStore(self, storeName, bank, address):
        try:
            return self.__market.createStore(storeName, self, bank, address)
        except Exception as e:
            raise Exception(e)

    @threaded
    def removeStore(self, storeId):
        try:
            return self.__market.removeStore(storeId, self)
        except Exception as e:
            raise Exception(e)

    @threaded
    def recreateStore(self, storeId):
        try:
            return self.__market.recreateStore(storeId, self)
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
    def setDiscountPermission(self, storeID, assignee):
        try:
            return self.__market.setDiscountPermission(storeID, self, assignee)
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
    def updateProductWeight(self, storeID, productID, newWeight):
        try:
            return self.__market.updateProductWeight(self, storeID, productID, newWeight)
        except Exception as e:
            raise Exception(e)

    @threaded
    def getRolesInformation(self, storeID):
        try:
            return self.__market.getRolesInformation(storeID, self)
        except Exception as e:
            raise Exception(e)

    @threaded
    def getPurchaseHistoryInformation(self, storeID):
        try:
            return self.__market.printPurchaseHistoryInformation(storeID, self)
        except Exception as e:
            raise Exception(e)

    def getUserStores(self):
        try:
            return self.__market.getUserStores(self)
        except Exception as e:
            raise Exception(e)

    @threaded
    def removeStoreOwner(self, storeId, assignee):
        try:
            return self.__market.removeStoreOwner(storeId, self, assignee)
        except Exception as e:
            raise Exception(e)

    @threaded
    def hasRole(self):
        try:
            return self.__market.hasRole(self)
        except Exception as e:
            raise Exception(e)

    @threaded
    def hasDiscountPermission(self, storeId):
        try:
            return self.__market.hasDiscountPermission(self, storeId)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addSimpleDiscount(self, storeId, discount):
        try:
            return self.__market.addSimpleDiscount(self, storeId, discount)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addCompositeDiscount(self, storeId, discountId, dId1, dId2, typeDiscount, decide):
        try:
            return self.__market.addCompositeDiscount(self, storeId, discountId, dId1, dId2, typeDiscount, decide)
        except Exception as e:
            raise Exception(e)

    @threaded
    def removeDiscount(self, storeId, discountId):
        try:
            return self.__market.removeDiscount(self, storeId, discountId)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addSimpleRuleDiscount(self, storeId, dId, rule):
        try:
            return self.__market.addSimpleRuleDiscount(self, storeId, dId, rule)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addCompositeRuleDiscount(self, storeId, dId, ruleId, rId1, rId2, ruleType):
        try:
            return self.__market.addCompositeRuleDiscount(self, storeId, dId, ruleId, rId1, rId2, ruleType)
        except Exception as e:
            raise Exception(e)

    @threaded
    def removeRuleDiscount(self, storeId, dId, rId):
        try:
            return self.__market.removeRuleDiscount(self, storeId, dId, rId)
        except Exception as e:
            raise Exception(e)
