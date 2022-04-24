import uuid

from Business.StorePackage.Store import Store
from interfaces.IGuest import Guest
from interfaces.IMarket import IMarket
from interfaces.IMember import Member
from interfaces.IStore import IStore
from Business.UserPackage.User import User
from Business.StorePackage.Product import Product
from interface import implements
from typing import Dict


def singleton_dec(class_):
    instances = {}

    def getInstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getInstance


@singleton_dec
class Market(implements(IMarket)):
    def __init__(self):
        self.__stores: Dict[int, IStore] = {}  # <id,Store> should check how to initial all the stores into dictionary
        self.__activeUsers: Dict[str, User] = {}  # <name,User> should check how to initial all the activeStores into dictionary
        self.__products: Dict[int, Product] = {}

    def __checkOnlineMember(self, userName):
        if (self.__activeUsers.get(userName)) is None:
            raise Exception("The member " + userName + " not online!")

    def createStore(self, storeName, userID, bank, address):
        if self.checkOnlineMember(userID):
            storeID = uuid.uuid4()
            userID = self.__activeUsers.get(userID)
            if userID is not None:
                newStore = Store(storeID, storeName, userID, bank, address)
                self.__stores[storeID] = newStore
                return storeID
        return False

    def addGuest(self):  # ?
        guest = Guest()
        self.__activeUsers[guest.getUserID()] = guest
        return guest

    def addMember(self, userName, password, phone, address, bank):
        member = Member(userName, password, phone, address, bank)
        self.__activeUsers[member.getUserID()] = member
        return member

    #  action of buyers - market managment
    def addProductToCart(self, userID, storeID, product, quantity):
        try:
            if self.checkOnlineMember(userID) is not None:
                if self.__stores.get(storeID).addProductToBag(product.getProductId(), quantity):
                    self.__activeUsers.get(userID).getCart().addProduct(storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self, userID, storeID, product):
        try:
            if self.__activeUsers.get(userID):
                quantity = self.__activeUsers.get(userID).getCart().removeProductFromCart(userID, storeID, product)
                self.__stores.get(storeID).removeProductFromBag(product.getProductId(), quantity)
            else:
                raise Exception("user not online")
        except Exception as e:
            return e

    def updateProductFromCart(self, userID, storeID, product, quantity):
        try:
            if self.__activeUsers.get(userID):
                self.__activeUsers.get(userID).getCart().updateProduct(storeID, product.getProductId(), quantity)
                if quantity > 0:
                    self.__stores.get(storeID).addProductToBag(product.getProductId(), quantity)
                else:
                    self.__stores.get(storeID).removeProductFromBag(product.getProductId(), quantity)
            else:
                raise Exception("user not online")
        except Exception as e:
            return e

    def ChangeProductQuanInCart(self, userID, storeID, product, quantity):
        try:
            if self.__activeUsers.get(userID):
                self.__activeUsers.get(userID).getCart().changeProductFromCart(userID, storeID, product, quantity)
            else:
                raise Exception("user not online")
        except Exception as e:
            return e

    def addTransaction(self, storeID, transaction):
        try:
            self.__stores.get(storeID).addTransaction(transaction)
        except Exception as e:
            return e

    def removeTransaction(self, storeID, transaction):
        try:
            self.__stores.get(storeID).removeTransaction(transaction)
        except Exception as e:
            return e

    def getProductByCategory(self, category):
        productsInStores: Dict[IStore, Product] = {}
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByCategory(category)
            if products_list_per_Store is not None:
                productsInStores[self.__stores.get(i)] = products_list_per_Store
        return productsInStores

    def getProductsByName(self, nameProduct):
        productsInStores: Dict[IStore, Product] = {}
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByName(nameProduct)
            if products_list_per_Store is not None:
                productsInStores[self.__stores.get(i)] = products_list_per_Store
        return productsInStores

    def getProductByKeyWord(self, keyword):
        productsInStores: Dict[IStore, Product] = {}
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByKeyword(keyword)
            if products_list_per_Store is not None:
                productsInStores[self.__stores.get(i)] = products_list_per_Store
        return productsInStores

    def purchaseCart(self, userID, bank):
        pass

    #  action of roles - role managment
    def appointManagerToStore(self, storeID, assignerID, assigneeID):  # check if the asssignee he member and assignerID!!
        try:
            if self.__activeUsers.get(assignerID) is not None:
                self.__stores.get(storeID).appointManagerToStore(assignerID, assigneeID)
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            return e

    def appointOwnerToStore(self, storeID, assignerID, assigneeID):  # check if the assignee he member and assignerID!!
        try:
            if self.__activeUsers.get(assignerID) is not None:
                self.__stores.get(storeID).appointOwnerToStore(assigneeID, assigneeID)
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            return e

    def setStockManagerPermission(self, storeID, assignerID, assigneeID):
        try:
            if self.checkOnlineMember(assignerID) is not None:
                self.__stores.get(storeID).setAppointManagerPermission(assignerID, assigneeID)
        except Exception as e:
            return e

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID):
        try:
            if self.checkOnlineMember(assignerID) is not None:
                self.__stores.get(storeID).setAppointOwnerPermission(assignerID, assigneeID)
        except Exception as e:
            return e

    def setChangePermission(self, storeID, assignerID, assigneeID):
        try:
            if self.checkOnlineMember(assignerID) is not None:
                self.__stores.get(storeID).setChangePermission(assignerID, assigneeID)
        except Exception as e:
            return e

    def setRolesInformationPermission(self, storeID, assignerID, assigneID):
        try:
            if self.checkOnlineMember(assignerID) is not None:
                self.__stores.get(storeID).setRolesInformationPermission(assignerID, assigneID)
        except Exception as e:
            return e

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            if self.checkOnlineMember(assignerID) is not None:
                self.__stores.get(storeID).setPurchaseHistoryInformationPermission(assignerID, assigneeID)
        except Exception as e:
            return e

    def addProductToStore(self, storeID, userID, product):
        try:
            if self.checkOnlineMember(userID) is not None:
                self.__stores.get(storeID).addProductToStore(userID, product)
        except Exception as e:
            return e

    def updateProductFromStore(self, storeID, userID, productId, newProduct):
        try:
            if self.checkOnlineMember(userID) is not None:
                self.__stores.get(storeID).updateProductFromStore(userID, productId, newProduct)
        except Exception as e:
            return e

    def addProductQuantityToStore(self, storeID, userID, product, quantity):
        try:
            if self.checkOnlineMember(userID) is not None:
                self.__stores.get(storeID).addProductQuantityToStore(userID, product.getProductId(), quantity)
        except Exception as e:
            return e

    def removeProductFromStore(self, storeID, userID, product):
        try:
            if self.checkOnlineMember(userID) is not None:
                self.__stores.get(storeID).removeProductFromStore(userID, product.getProductId())
        except Exception as e:
            return e

    def printRolesInformation(self, storeID, userID):
        try:
            if self.checkOnlineMember(userID) is not None:
                self.__stores.get(storeID).PrintRolesInformation(userID)
        except Exception as e:
            return e

    def printPurchaseHistoryInformation(self, storeID, userID):
        try:
            self.__stores.get(storeID).printPurchaseHistoryInformation(userID)
        except Exception as e:
            return e
