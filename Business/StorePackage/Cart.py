import zope
from zope.interface import implements

from Exceptions.CustomExceptions import NoSuchStoreException, NoSuchBagException
from interfaces.ICart import ICart
from Business.StorePackage.Bag import Bag
from Business.StorePackage.Product import Product
from typing import Dict


@zope.interface.implementer(ICart)
class Cart:

    def __init__(self, userId):
        self.__userId = userId
        self.__bags: Dict[int, Bag] = {}  # storeId : Bag

    def getUserId(self):
        return self.__userId

    def getAllBags(self):
        return self.__bags

    def getBag(self, storeId):
        try:
            return self.__bags[storeId]
        except:
            raise NoSuchStoreException("storeId does not exists, can't add the bag to the cart")

    def removeBag(self, storeId):
        if self.__bags.get(storeId) is not None:
            self.__bags.pop(storeId)
            return True
        else:
            return False

    def cleanBag(self, storeId):
        if self.__bags.get(storeId) is not None:
            self.__bags.get(storeId).cleanBag()
        else:
            raise NoSuchStoreException("storeId does not exists, can't clean the bag from the cart")

    def updateCart(self, cart):
        for storeId in cart.getAllBags().keys():
            if storeId in self.__bags.keys():
                self.__bags[storeId] = self.__bags[storeId].addBag(cart.getAllBags()[storeId])
            else:
                self.__bags[storeId] = cart.getAllBags()[storeId]



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

    def calcSumOfBag(self, storeId):
        return self.__bags.get(storeId).calcSum()

    def isEmpty(self):
        for bag in self.__bags.values():
            if not bag.isEmpty():
                return False
        return True

    def addProduct(self, storeId, product, quantity):
        if self.__bags.get(storeId) is None:
            self.__bags[storeId] = Bag(storeId)
        self.getBag(storeId).addProduct(product, quantity)

    def removeProduct(self, storeId, productId):
        quantity = self.getBag(storeId).removeProduct(productId)
        if self.getBag(storeId).isEmpty():
            self.removeBag(storeId)
        return quantity

    def updateProduct(self, storeId, productId, quantity):  # quantity can be negative!!!
        if self.__bags.get(storeId) is None:
            raise NoSuchBagException("can't update a product without a bag to his store")
        self.getBag(storeId).updateProduct(productId, quantity)
        if self.getBag(storeId).isEmpty():
            self.removeBag(storeId)
        return True

    def cleanCart(self):
        for bag in self.__bags.values():
            bag.cleanBag()

    def getAllProductsByStore(self):
        products: Dict[int, Dict[Product, int]] = {}  # [storeId: [product : quantity]]
        for bag in self.__bags.values():
            products.update({bag.getStoreId(): bag.getProducts()})
        return products

    def getAllProducts(self):
        products: Dict[Product, int] = {}  # [product : quantity]
        for bag in self.__bags.values():
            products.update(bag.getProducts())
        return products

    def printBags(self):
        printBags = ""
        for bag in self.__bags.values():
            printBags += "\n\t\t\tStore id:" + str(
                bag.getStoreId()) + " store products:" + "\t\t\t\t\t\t\t\t\t" + bag.printProducts()
        return printBags

    def applyDiscount(self, bag: Bag):
        bag.applyDiscount()

