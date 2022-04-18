from interfaces.IStore import IStore
from interfaces.ICart import ICart
from  interfaces import IMarket
from Business.UserPackage.User import User
from Business.UserPackage.Member import Member
from typing import Dict
class Market(IMarket):
    def __init__(self):
        self.__stores : Dict[int,IStore] = {} # <id,Store> should check how to initial all the stores into dictionary
        self.__activeUsers : Dict[str,User] = {} # <name,User> should check how to initial all the activeStores into dictionary
        self.__membersFromCart : Dict[str, Member] ={}  # <name,Icart> should check how to initial all the stores into dictionary
        self.__history = {} #need be replace by instance
    def getStoreByName(self,store_name:str):
        store_collection = []
        for store in self.__stores:
            name : Dict[str]=store.getStoreName(store_name)
            if(name == store_name) :
                store_collection.append(store)
        return  store_collection


    def getStoreById(self,id_store): #maybe should be private
        return self.__stores.get(id_store)
    def getProductByCatagory(self,catagory):
        product_collection =[]
        for store in self.__stores:
            product_collection.append(store.getProductByCatagory(catagory))
        return  product_collection


    def getProductByName(self,name):
        product_collection = []
        for store in self.__stores:
            product_collection.append(store.getProductByName(name))
        return product_collection

    def getProductByKeyWord(self, keyword):
        product_collection = []
        for store in self.__stores:
            product_collection.append(store.getProductByKeyWord(keyword))
        return product_collection

    def getUserByName(self,userName):
        return self.__activeUsers.get(userName)

    def createStore(self,storeName, userName, bankAccount, address):
        pass

    def addComment(self, productID, comment):
        pass

    def addProductRating(self, productID, rating):
        pass

    def addStoreRating(self,storeID, rating):
        pass

    def contactToStore(self,userName,store,comment):
        pass

    def complaint(self):
        pass

    def getMemberHistory(self,nameMember):
        member = self.__membersFromCart.get(self.getUserByName(nameMember))
        return member.getMemberHistory()

    def getStoreHistory(self,userName,storeID):
        pass
    def addProductToCart(self,username,id_prod,product_name,qantity):
        pass
    def removeProductFromCart( username,product) :
        pass

    def ChangeProductQuanInCart(self,username,product,qantity):
        pass
    def updateCart(self, username, removed_product, addedProducts, products_quantity):
        ans =  []
        user = self.getUserByName(username)
        if(user is not none):
            for(product in addedProducts):
                self.addProductToCart(product)
            for( product in removed_product):
                self.removeProductFromCart(username,product)
            for(product )


