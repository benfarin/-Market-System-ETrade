from interface import implements
from interfaces import IBag


class Bag(implements(IBag)):

    def __init__(self):
        self.products = dict()  # product : quantity

    def isEmpty(self):
        pass

    def addProduct(self, productId, quantity):
        pass

    def removeProduct(self, productId):
        pass

    def removeProductQuantity(self, productId, quantity):
        pass

    def getProducts(self):
        pass

    def getProductQuantity(self, productId):
        pass

    def calcSum(self):
        pass
