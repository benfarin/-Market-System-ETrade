import uuid

from Business.StorePackage.Store import Store
from Business.UserPackage.Guest import Guest
from Business.UserPackage.Member import Member
from interfaces.IMarket import IMarket
from interfaces.IStore import IStore
from Business.UserPackage.User import User
from Business.StorePackage.Product import Product
from interface import implements
from typing import Dict


class Market(implements(IMarket)):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Market.__instance is None:
            Market()
        return Market.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__stores: Dict[int, IStore] = {}  # <id,Store> should check how to initial all the stores into dictionary
        self.__activeUsers: Dict[str, User] = {}  # <name,User> should check how to initial all the activeStores into dictionary
        self.__products: Dict[int, Product] = {}
        self.__globalStore = 0
        if Market.__instance is None:
            Market.__instance = self

    def __checkOnlineUser(self, userName):
        if (self.__activeUsers.get(userName)) is None:
            raise Exception("The member " + userName + " not online!")
        else:
            return True

    def createStore(self, storeName, userID, bank, address):
        if self.__checkOnlineUser(userID):
            storeID = self.__globalStore + 1
            newStore = Store(storeID, storeName, userID, bank, address)
            self.__stores[storeID] = newStore
            return newStore
        return None

    def addGuest(self):  # ?
        guest = Guest()
        self.__activeUsers[guest.getUserID()] = guest
        return guest


    def addActiveUser(self,user):
        try:
             self.__activeUsers[user.getUserID()] = user
             return True
        except:
            return False




    #  action of buyers - market managment
    def addProductToCart(self, userID, storeID, productID , quantity): #Tested
        try:
            if self.__checkOnlineUser(userID) is not None:
                if self.__products.get(productID) is None:
                    raise Exception("The product id " + productID + " not in market!")
                if self.__stores.get(storeID).addProductToBag(productID, quantity):
                    self.__activeUsers.get(userID).getCart().addProduct(storeID, self.__products.get(productID), quantity)
                    return True
                else:
                    raise Exception("The quantity " + quantity + " is not available")
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self,storeID ,userID, productId): #Tested
        try:
            if self.__activeUsers.get(userID):
                quantity = self.__activeUsers.get(userID).getCart().removeProduct(storeID, productId)
                self.__stores.get(storeID).removeProductFromBag(productId, quantity)
                return True
            else:
                raise Exception("user not online")
        except Exception as e:
            return e

    def updateProductFromCart(self, userID, storeID, productId, quantity): #UnTested
        try:
            if self.__activeUsers.get(userID):
                if self.__products.get(productId) is None:
                    raise Exception("The product id " + productId + " not in market!")
                if quantity > 0:
                    return self.addProductToCart(userID, storeID, productId, quantity)
                else:
                    return self.removeProductFromBag(productId, quantity)
            else:
                raise Exception("user not online")
        except Exception as e:
            return e

    #  def ChangeProductQuanInCart(self, userID, storeID, product, quantity):
    #     try:
    #        if self.__activeUsers.get(userID):
    #            self.__activeUsers.get(userID).getCart().changeProductFromCart(userID, storeID, product, quantity)
    #        else:
    #            raise Exception("user not online")
    #    except Exception as e:
    #        return e

    def addTransaction(self, storeID, transaction):
        try:
            self.__stores.get(storeID).addTransaction(transaction)
        except Exception as e:
            raise Exception(e)

    def removeTransaction(self, storeID, transaction):
        try:
            self.__stores.get(storeID).removeTransaction(transaction)
        except Exception as e:
            raise Exception(e)

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
    def appointManagerToStore(self, storeID, assignerID,assigneeID):  # Tested
        try:
            if self.__activeUsers.get(assignerID) is not None:
                self.__stores.get(storeID).appointManagerToStore(assignerID, assigneeID)
                return True
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assignerID, assigneeID):  # unTested
        try:
            if self.__activeUsers.get(assignerID) is not None:
                self.__stores.get(storeID).appointOwnerToStore(assignerID, assigneeID)
                return True
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assignerID, assigneeID): #Tested
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setStockManagementPermission(assignerID, assigneeID)
                return True
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID): #Tested
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setAppointOwnerPermission(assignerID, assigneeID)
                return True
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assignerID, assigneeID):
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setChangePermission(assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setRolesInformationPermission(assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setPurchaseHistoryInformationPermission(assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def addProductToStore(self, storeID, userID, product): #Tested
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).addProductToStore(userID, product)
                if self.__products.get(product.getProductId) is None:
                    self.__products[product.getProductId()] = product
                return True
            else:
                raise Exception("member with id " + userID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def updateProductFromStore(self, storeID, userID, productId, newProduct):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).updateProductFromStore(userID, productId, newProduct)
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).addProductQuantityToStore(userID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, userID, product):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).removeProductFromStore(userID, product.getProductId())
        except Exception as e:
            raise Exception(e)

    def printRolesInformation(self, storeID, userID):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).PrintRolesInformation(userID)
        except Exception as e:
            raise Exception(e)

    def printPurchaseHistoryInformation(self, storeID, userID):
        try:
            self.__stores.get(storeID).printPurchaseHistoryInformation(userID)
        except Exception as e:
            raise Exception(e)

        def checkOnlineMember(self, userName):
            if (self.__activeUsers.get(userName)) == None:
                raise Exception("The member " + userName + " not online!")

    def getStoreByName(self, store_name):
        store_collection = []
        store_names = self.__stores.keys()
        for s in store_names:
            if (self.__stores.get(s).getName() == store_name):
                store_collection.append(self.__stores.get(s))
        return store_collection

    def getStoreById(self, id_store):  # maybe should be private
        return self.__stores.get(id_store)

    def getUserByName(self, userName):
        return self.__activeUsers.get(userName)

    def getStores(self):
        return self.__stores

    def getActiveUsers(self):
        return self.__activeUsers

    def getProducts(self):
        return self.__products


