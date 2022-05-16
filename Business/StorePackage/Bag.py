import zope
from zope.interface import implements

from Exceptions.CustomExceptions import QuantityException, ProductException
from interfaces.IBag import IBag
from Business.StorePackage.Predicates.StorePredicateManager import storePredicateManager


@zope.interface.implementer(IBag)
class Bag:

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
            raise QuantityException("cannot add negative quantity of product")
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
        raise ProductException("no such product in the Bag")

    def updateBag(self, productId, quantity):
        for product in self.__products.keys():
            if product.getProductId() == productId:
                self.__products[product] += quantity
                if self.__products[product] <= 0:
                    self.__products.pop(product)
                return True
        raise ProductException("no such product in the Bag")

    def getProducts(self):
        return self.__products

    def addBag(self, bag):
        for product in bag.__products.keys():
            if product in self.__products:
                self.__products[product] += bag.getProducts()[product]
            else:
                self.__products[product] = bag.getProducts()[product]
        return True

    def getProductQuantity(self, product):
        return self.__products[product]

    def calcSum(self):
        return self.applyDiscount()

    def cleanBag(self):
        self.__products = {}

    def printProducts(self):
        products_print = ""
        for product in self.__products:
            products_print += "\n\t\t\tid product:" + str(product.getProductId()) + " name:" + str(
                product.getProductName()) + " quantity:" + str(self.__products.get(product))
        return products_print

    def __searchProductByProductId(self, pId):
        for product in self.__products.keys():
            if product.getProductId() == pId:
                return product
        return None

    def applyDiscount(self):
        # discounts = storePredicateManager.getInstance().getDiscountsByIdStore(self.__storeId)  # brings all of the discounts of the store
        # if discounts is None:
        #     newPrices = {}
        #     for product in self.__products:
        #         newPrices[product] = product.getProductPrice() * self.__products[product]
        #     return newPrices
        # discounts = storePredicateManager.getInstance().getDiscountsByIdStore(self.__storeId)  # brings all of the discounts of the store
        # for product in self.__products:
        #     sum += product.applyDiscount(self)
        # return sum

        discounts = storePredicateManager.getInstance().getDiscountsByIdStore(self.__storeId)  # brings all of the discounts of the store
        if discounts is None:
            newPrices = {}
            for product in self.__products:
                newPrices[product] = product.getProductPrice() * self.__products[product]
            return newPrices
        f = lambda discount: discount.getRule().check(self)
        minPrice = float('inf')
        for discount in discounts:
            if f(discount):
                newPrice = self.findMinBagPrice(discount.makeDiscount(self))
                if newPrice < minPrice:
                    minPrice = newPrice
        return minPrice

    def findMinBagPrice(self, discount_of_product):
        newPrices = discount_of_product.getProducts()
        s = 0
        for prod in newPrices.keys():
            s += newPrices[prod] * prod.getProductPrice() * self.__products.get(prod)
        return s





