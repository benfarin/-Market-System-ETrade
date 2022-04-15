from interface import implements
from interfaces.IBag import IBag


class Bag(implements(IBag)):

    def __init__(self, cart, storeId):
        self.__cart = cart
        self.__storeId = storeId
        self.__products = {}  # product : quantity

    def isEmpty(self):
        return len(self.__products) == 0

    def getStoreId(self):
        return self.__storeId

    def addProduct(self, product, quantity):
        if quantity <= 0:
            raise Exception("cannot add negative quantity of product")
        # check if the product is available
        if self.__products.get(product) is None:
            self.__products[product] = quantity
            return True
        self.__products[product] = self.__products[product] + quantity
        self.__cart.updateBag(self)
        return True

    def removeProduct(self, productId):
        for product in self.__products.keys():
            if product.getProductId() == productId:
                self.__products.pop(product)
                self.__cart.updateBag(self)
                return True
        raise Exception("no such product in the Bag")

    def removeProductQuantity(self, productId, quantity):
        if quantity < 0:
            raise Exception("cannot remove negative quantity of product")
        for product in self.__products.keys():
            if product.getProductId() == productId:
                self.__products[product] -= quantity
                if self.__products[product] <= 0:
                    self.__products.pop(product)
                self.__cart.updateBag(self)
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

