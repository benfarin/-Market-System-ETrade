from interface import implements
from interfaces.IBag import IBag


class Bag(implements(IBag)):

    def __init__(self):
        self.__products = {}  # product : quantity

    def isEmpty(self):
        return len(self.__products) == 0

    def addProduct(self, product, quantity):
        if quantity <= 0:
            return False
        # check if the product is available
        if self.__products.get(product) is None:
            self.__products[product] = quantity
            return True
        self.__products[product] = self.__products[product] + quantity
        return True

    def removeProduct(self, productId):
        for product in self.__products.keys():
            if product.getProductId() == productId:
                self.__products.pop(product)
                return True
        return False

    def removeProductQuantity(self, product, quantity):
        if self.__products[product] is None:
            return False
        self.__products[product] = self.__products[product] - quantity
        if self.__products[product] <= 0:
            self.removeProduct(product.getProductId())

    def getProducts(self):
        return self.__products

    def getProductQuantity(self, product):
        return self.__products[product]

    def calcSum(self):
        s = 0.0
        for p in self.__products.keys():
            s += p.getProductPrice() * self.__products[p]
        return s