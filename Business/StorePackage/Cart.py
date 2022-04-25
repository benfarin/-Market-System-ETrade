from interface import implements
from interfaces.ICart import ICart
from Business.StorePackage.Bag import Bag
from Business.StorePackage.Product import Product
from typing import Dict


class Cart(implements(ICart)):

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
            raise Exception("storeId does not exists, can't add the bag to the cart")

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
            raise Exception("can't update a product without a bag to his store")
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
<<<<<<< HEAD
    def checkPolicy(self):
        pass

    def purchase(self,clienID,clientBankAccount,clientphone,clientadress,sumToPay):
        purchase = {}
        for bag  in self.__bag:
            purchaseStatus =  bag.getStore().p


=======

    def getAllProducts(self):
        products: Dict[Product, int] = {}  # [product : quantity]
        for bag in self.__bags.values():
            products.update(bag.getProducts())
        return products
>>>>>>> 467c252b2ec8b4dd444758cfe108d5883b34efab
