from interface import implements
from interfaces.IBag import IBag


class Bag(implements(IBag)):

    def __init__(self, storeId):
        self.__storeId = storeId
        self.__products = {}  # product : quantity

    def getStore(self):
        pass
    def isEmpty(self):
        return len(self.__products) == 0

    def getStoreId(self):
        return self.__storeId

    def getBag(self):
        return self

    def addProduct(self, product, quantity):
        if quantity <= 0:
            raise Exception("cannot add negative quantity of product")
        if self.__products.get(product) is None:
            self.__products[product] = quantity
            return True
        self.__products[product] = self.__products[product] + quantity
        return True

    def removeProduct(self, productId):
        for product in self.__products.keys():
            if product.getProductId() == productId:
                quantity = self.__products[product]
                self.__products.pop(product)
                return quantity
        raise Exception("no such product in the Bag")

    def updateProduct(self, productId, quantity):
        for product in self.__products.keys():
            if product.getProductId() == productId:
                self.__products[product] += quantity
                if self.__products[product] <= 0:
                    self.__products.pop(product)
                return True
        raise Exception("no such product in the Bag")

    def getProducts(self):
        return self.__products

    def getProductQuantity(self, product):
        return self.__products[product]

    def calcSum(self):
        s = 0.0
        for p in self.__products.keys():
            s += p.getProductPrice() * self.__products[p]
        return s

    def cleanBag(self):
        self.__products = {}

    def printProducts(self):
        products_print = ""
        for product in self.__products:
            products_print += "\n\t\t\tid product:" + str(product.getProductId()) + " name:" + str(product.getProductName()) + " quantity:" + str(self.__products.get(product))
        return products_print
