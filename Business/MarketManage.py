from interfaces.IStore import IStore
from Business.StorePackage.Store import Store
from interfaces.ICart import ICart
from  interfaces import IMarket
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
            self.__membersFromCart : Dict[str,ICart] ={}  # <name,Icart> should check how to initial all the stores into dictionary
            self.__history = {} #need be replace by instance
            self.__products : Dict [int,Product]  = {}

    def checkOnlineMember(self, userName):
        for key in self.__membersFromCart.keys():
            if (userName == key):
                if (self.__activeUsers.get(key)):
                    return True
        return False

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

    def createStore(self,storeName, userName, bankAccount, address):
        if (self.checkOnlineMember(userName)):
            storeID = uuid.uuid4()
            userID = self.__activeUsers.get(userName)
            if(userID != None):
                newStore = Store(storeID,storeName, userID)
                self.__stores[storeID] = newStore
                return True
        return False

    def addProductToCart(self,username,storeID ,product,quantity):
        try:
            if(self.__activeUsers.get(username) ):
                if (self.__stores.get(storeID).addProductToBag(product.getProductId(),quantity)) :
                    bag : Bag= self.__membersFromCart.get(username).getBag(storeID)
                    bag.addProduct(product,quantity)
        except Exception as e :
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
        self.__membersFromCart[member.getUserID()] = member.getShoppingCart() # maybe need to remove
        return member

    def getStoreHistory(self,userName,storeID):
        pass

    def removeProductFromCart(self,userName,storeID ,product):
        try:
            if self.__activeUsers.get(userName):
                self.__activeUsers.get(userName).getShoppingCart().removeProductFromCart(userName,storeID,product)
            else:
                raise Exception ("user not online")
        except Exception as e:
            return e
    def ChangeProductQuanInCart(self,userName,storeID,product,quantity):
        try:
            if self.__activeUsers.get(userName):
                self.__activeUsers.get(userName).getShoppingCart().changeProductFromCart(userName, storeID, product,quantity)
            else:
                raise Exception("user not online")
        except Exception as e:
            return e
    def updateCart(self, username, removed_product, addedProducts, products_quantity):
       pass

