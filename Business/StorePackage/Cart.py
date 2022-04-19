from interface import implements
from interfaces.ICart import ICart
from Business.StorePackage.Bag import Bag
from typing import Dict

class Cart(implements(ICart)):

    def __init__(self, userId):
        self.__userId = userId
        self.__bags : Dict[int,Bag] = {}  # storeId : Bag

    def getUserId(self):
        return self.__userId

    def getAllBags(self):
        return self.__bags

    def getBag(self, storeId):
        try:
            return self.__bags[storeId]
        except:
            raise Exception("storeId does not exists, can't add the bag to the cart")

    def addBag(self, storeId):
        if self.__bags.get(storeId) is None:
            self.__bags[storeId] = Bag(self, storeId)
            return True
        else:
            return False

    def removeBag(self, storeId):
        if self.__bags.get(storeId) is not None:
            self.__bags.pop(storeId)
            return True
        else:
            return False

    def updateBag(self, bag):
        if self.__bags.get(bag.getStoreId()) is not None:
            self.__bags[bag.getStoreId()] = bag
            return True
        else:
            return False

    def calcSum(self):
        s = 0.0
        for bag in self.__bags.values():
            s += bag.calcSum()
        return s

    def getAllProduct(self):
        products = {}
        for bag in self.__bags.values():
            products.setdefault(bag.getProducts())
        return products

    def isEmpty(self):
        for bag in self.__bags.values():
            if not bag.isEmpty():
                return False
        return True

    def addProduct(self, storeID, product, quantity):
        self.getBag(storeID).addProduct(product, quantity)

    def removeProduct(self, storeID, product):
        self.getBag(storeID).removeProduct(product)

    def updateProduct(self, storeID, productId, quantity):  # quantity can be negative!!!
        self.getBag(storeID).updateProduct(productId, quantity)

