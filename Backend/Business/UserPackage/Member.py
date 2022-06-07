from Backend.Business.Address import Address
from Backend.Business.Bank import Bank
from Backend.Business.StorePackage.Cart import Cart
from Backend.Business.UserPackage.User import User
import bcrypt
import threading
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from Backend.Exceptions.CustomExceptions import NoSuchMemberException, PasswordException
from Backend.Interfaces.IMarket import IMarket
import Backend.Business.Market as m
from concurrent.futures import Future

from ModelsBackend.models import MemberModel, CartModel, BagModel, UserTransactionModel
from django.contrib.auth.hashers import make_password, check_password



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
    def __init__(self, userName=None, password=None, phone=None, address=None, bank=None, model=None):  # extend the constructor of user class
        # self.__isLoggedIn = False
        # self.__userName = userName  # string
        # self.__password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # string
        # self.__phone = phone  # string
        # self.__address : Address = address  # type address class
        # self.__bank :Bank = bank  # type bank
        self.__market: IMarket = m.Market.getInstance()
        if model is None:
            super().__init__()
            self._m = MemberModel.objects.get_or_create(userid=super().getUserID(),
                                                         member_password=make_password(password),
                                                         phone=phone, address=address.getModel(), bank=bank.getModel(),
                                                         cart=super().getCart().getModel())[0]
            super().setUsername(userName)
        else:
            super().__init__(model)
            self._m = model

    def setLoggedIn(self, state):
        super().setLoggedIn(state)

    def addProductRating(self, productID, rating):
        pass

    def getPassword(self):
        return self._m.member_password

    def getPhone(self):
        return self._m.phone

    def getAddress(self):
        return Address(model=self._m.address)

    def getBank(self):
        return Bank(model=self._m.bank)

    def getMemberName(self):
        return super().getUsename()

    def getMemberTransactions(self):
        return super().getTransactions().values()

    def setCart(self, cart):
        self._m.cart = cart.getModel()
        self._m.save()

    def updateCart(self, cart):
        oldCart = self._buildCart(self._m.cart)
        self.__market.updateCart(oldCart, cart)

    def isStoreExists(self, storeId):
        return self.__market.isStoreExists(storeId)

    def loginUpdates(self):
        try:
            super().loginUpdates()
            return self.__market.loginUpdates(self)
        except Exception as e:
            raise Exception(e)

    def change_password(self, old_password, new_password):
        if bcrypt.checkpw(old_password.encode('utf-8'), self._m.password):
            self._m.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self._m.save()
            return "Password changed succesfully!"
        else:
            raise PasswordException("password not good!")

    def getModel(self):
        return self._m

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
    def removeStoreForGood(self, storeId):
        try:
            return self.__market.removeStoreForGood(storeId, self)
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
            return self.__market.updateProductPrice(self, storeID, productId, newPrice)
        except Exception as e:
            raise Exception(e)

    @threaded
    def updateProductName(self, storeID, productID, newName):
        try:
            return self.__market.updateProductName(self, storeID, productID, newName)
        except Exception as e:
            raise Exception(e)

    @threaded
    def updateProductCategory(self, storeID, productID, newCategory):
        try:
            return self.__market.updateProductCategory(self, storeID, productID, newCategory)
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
            return self.__market.getPurchaseHistoryInformation(storeID, self)
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
    def addSimpleRule(self, storeId, dId, rule):
        try:
            return self.__market.addSimpleRule(self, storeId, dId, rule)
        except Exception as e:
            raise Exception(e)

    @threaded
    def addCompositeRule(self, storeId, dId, ruleId, rId1, rId2, ruleType, ruleKind):
        try:
            return self.__market.addCompositeRule(self, storeId, dId, ruleId, rId1, rId2, ruleType, ruleKind)
        except Exception as e:
            raise Exception(e)

    @threaded
    def removeRule(self, storeId, dId, rId, ruleKind):
        try:
            return self.__market.removeRule(self, storeId, dId, rId, ruleKind)
        except Exception as e:
            raise Exception(e)

    def removeUser(self):
        super().removeUser()
        self._m.delete()

    def _buildCart(self, model):
        return Cart(model=model)

    def __eq__(self, other):
        return isinstance(other, Member) and self._m == other.getModel()

    def __hash__(self):
        return hash(self._m.userid)

