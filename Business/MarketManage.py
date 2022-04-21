from interfaces.IStore import IStore
from Business.StorePackage.Store import Store
from interfaces.ICart import ICart
from  interfaces.IMarket import IMarket
from interface import implements
from Business.UserPackage.User import User
from Business.UserPackage.Member import Member
from Business.StorePackage.Product import Product
from Business.StorePackage.Bag import Bag
from Business.UserPackage.Guest import Guest
from typing import Dict
import uuid
def singleton_dec(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton_dec
class MarketManage(implements(IMarket)):
    def __init__(self):
            self.__stores : Dict[int,IStore] = {} # <id,Store> should check how to initial all the stores into dictionary
            self.__activeUsers : Dict[str,User] = {} # <name,User> should check how to initial all the activeStores into dictionary
            self.__products : Dict [int,Product]  = {}

    def checkOnlineMember(self, userName):
            if (self.__activeUsers.get(userName)) == None:
                raise Exception("The member " + userName + " not online!")
    def getStoreByName(self,store_name):
        store_collection = []
        store_names = self.__stores.keys()
        for s in store_names:
            if(self.__stores.get(s).getName()==store_name):
                store_collection.append(self.__stores.get(s))
        return store_collection

    def getStoreById(self,id_store): #maybe should be private
        return self.__stores.get(id_store)

    def getProductByCatagory(self,catagory):
        productsInStores: Dict[IStore, Product] = {}
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByCategory(catagory)
            if (products_list_per_Store != None):
                productsInStores[self.__stores.get(i)] = products_list_per_Store
        return productsInStores

    def getProductsByName(self,nameProduct):
        productsInStores:Dict[IStore,Product]={}
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByName(nameProduct)
            if(products_list_per_Store !=None):
                productsInStores[self.__stores.get(i)] = products_list_per_Store
        return productsInStores

    def getProductByKeyWord(self, keyword):
        productsInStores: Dict[IStore, Product] = {}
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByKeyword(keyword)
            if (products_list_per_Store != None):
                productsInStores[self.__stores.get(i)] = products_list_per_Store
        return productsInStores

    def getUserByName(self,userName):
        return self.__activeUsers.get(userName)

    def createStore(self,storeName, userID ,bank ,address):
        if (self.checkOnlineMember(userID)):
            storeID = uuid.uuid4()
            userID = self.__activeUsers.get(userID)
            if(userID != None):
                newStore = Store(storeID,storeName,userID,bank,address)
                self.__stores[storeID] = newStore
                return storeID
        return False

    def addProductToCart(self,userID ,storeID ,product , quantity):
        try:
            if(self.checkOnlineMember(userID) != None):
                if (self.__stores.get(storeID).addProductToBag(product.getProductId(),quantity)) :
                    self.__activeUsers.get(userID).getCart().addProduct(storeID,product,quantity)
        except Exception as e:
            raise Exception(e)

    def getStores(self):
        return self.__stores

    def getActiveUsers(self):
        return self.__activeUsers

    def getProducts(self):
        return self.__products

    def addGuest(self):
        guest = Guest()
        self.__activeUsers[guest.getUserID()] = guest
        return guest

    def addMember(self,userName, password, phone, address, bank):
        member = Member(userName, password, phone, address, bank)
        self.__activeUsers[member.getUserID()] = member
        return member

    def getStoreHistory(self,userName,storeID): # --------------------------------------------------
        if (self.__activeUsers.get(userName) != None):
            self.__stores.get(storeID).getPurchaseHistoryInformation()

    def removeProductFromCart(self,userID,storeID ,product):
        try:
            if self.__activeUsers.get(userID):
                quantity = self.__activeUsers.get(userID).getCart().removeProductFromCart(userID,storeID,product)
                self.__stores.get(storeID).removeProductFromBag(product.getProductId(),quantity)
            else:
                raise Exception ("user not online")
        except Exception as e:
            return e

    def updateProductFromCart(self,userID,storeID,product,quantity):
        try:
            if self.__activeUsers.get(userID):
                self.__activeUsers.get(userID).getCart().updateProduct(storeID, product.getProductId(),quantity)
                if quantity > 0 :
                    self.__stores.get(storeID).addProductToBag(product.getProductId(),quantity)
                else:
                    self.__stores.get(storeID).removeProductFromBag(product.getProductId(),quantity)
            else:
                raise Exception("user not online")
        except Exception as e:
            return e

    def ChangeProductQuanInCart(self,userID,storeID,product,quantity):
        try:
            if self.__activeUsers.get(userID):
                self.__activeUsers.get(userID).getCart().changeProductFromCart(userID, storeID, product,quantity)
            else:
                raise Exception("user not online")
        except Exception as e:
            return e

    def appointManagerToStore(self,storeID, assignerID , assigneID ): # check if the asssigne he member and assignerID!!
        try:
            if (self.__activeUsers.get(assignerID) != None) :
                self.__stores.get(storeID).appointManagerToStore(assigneID,assigneID)
            else:
                raise Exception("member with id "+ assignerID +" is not online!")
        except Exception as e:
            return e
    def appointOwnerToStore(self,storeID, assignerID , assigneID):# check if the asssigne he member and assignerID!!
        try:
            if (self.__activeUsers.get(assignerID) != None):
                self.__stores.get(storeID).appointOwnerToStore(assigneID, assigneID)
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            return e

    def setStockManagerPermission(self,storeID ,assignerID, assigneID):
       try:
           if self.checkOnlineMember(assignerID) != None :
               self.__stores.get(storeID).setAppointManagerPermission(assignerID,assigneID)
       except Exception as e:
           return e

    def setAppointOwnerPermission(self,storeID ,assignerID, assigneID):
        try:
            if self.checkOnlineMember(assignerID) != None:
                self.__stores.get(storeID).setAppointOwnerPermission(assignerID, assigneID)
        except Exception as e:
            return e

    def setChangePermission(self,storeID, assignerID, assigneID):
        try:
            if self.checkOnlineMember(assignerID) != None:
                self.__stores.get(storeID).setChangePermission(assignerID, assigneID)
        except Exception as e:
            return e

    def setRolesInformationPermission(self,storeID, assignerID, assigneID):
        try:
            if self.checkOnlineMember(assignerID) != None:
                self.__stores.get(storeID).setRolesInformationPermission(assignerID, assigneID)
        except Exception as e:
            return e

    def setPurchaseHistoryInformationPermission(self,storeID, assignerID, assigneID):
        try:
            if self.checkOnlineMember(assignerID) != None:
                self.__stores.get(storeID).setPurchaseHistoryInformationPermission(assignerID, assigneID)
        except Exception as e:
            return e

    def addProductToStore(self,storeID , userID, product):
        try:
            if self.checkOnlineMember(userID) != None:
                self.__stores.get(storeID).addProductToStore(userID, product)
        except Exception as e:
            return e

    def addProductQuantityToStore(self, storeID ,userID,product, quantity):
        try:
            if self.checkOnlineMember(userID) != None:
                self.__stores.get(storeID).addProductQuantityToStore(userID, product.getProductId(),quantity)
        except Exception as e:
            return e

    def removeProductFromStore(self,storeID , userID, product):
        try:
            if self.checkOnlineMember(userID) != None:
                self.__stores.get(storeID).removeProductFromStore(userID, product.getProductId())
        except Exception as e:
            return e

    def PrintRolesInformation(self,storeID ,userID):
        try:
            if self.checkOnlineMember(userID) != None:
                self.__stores.get(storeID).PrintRolesInformation(userID)
        except Exception as e:
            return e

    def addTransaction(self,storeID ,transaction):
        try:
            self.__stores.get(storeID).addTransaction(transaction)
        except Exception as e:
            return e

    def removeTransaction(self,storeID ,transaction):
        try:
            self.__stores.get(storeID).removeTransaction(transaction)
        except Exception as e:
            return e

    def printPurchaseHistoryInformation(self,storeID ,userID):
        try:
            self.__stores.get(storeID).printPurchaseHistoryInformation(userID)
        except Exception as e:
            return e

    def updateProductFromStore(self, userID, productId, newProduct):
        pass

    def removeBag(self,storeID,userID):
        try:
            if (self.__activeUsers.get(userID) != None):
                return self.__activeUsers.get(userID).getCart().removeBag(storeID)
            else:
                raise Exception("The user is not online!")
        except Exception as e:
            return e

    def updateBag(self,bag,userID):
        try:
            if (self.__activeUsers.get(userID) != None):
                return self.__activeUsers.get(userID).getCart().updateBag(bag)
            else:
                raise Exception("The user is not online!")
        except Exception as e:
            return e

    def getAllProducts(self,userID):
        try:
            if (self.__activeUsers.get(userID) != None):
                return self.__activeUsers.get(userID).getCart().getAllProduct()
            else:
                raise Exception("The user is not online!")
        except Exception as e:
            return e

    def isEmpty(self,userID):
        try:
            if (self.__activeUsers.get(userID) != None):
                return self.__activeUsers.get(userID).getCart().isEmpty()
            else:
                raise Exception("The user is not online!")
        except Exception as e:
            return e

    def calcSum(self,userID):
        try:
            if (self.__activeUsers.get(userID) != None):
                return self.__activeUsers.get(userID).getCart().calcSum()
            else:
                raise Exception("The user is not online!")
        except Exception as e:
            return e

    def getBag(self, storeId):
        pass

    def getAllBags(self):
        pass








