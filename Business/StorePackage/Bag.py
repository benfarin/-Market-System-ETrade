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

    def updateProduct(self, productId, quantity):
        for product in self.__products.keys():
            if product.getProductId() == productId:
                self.__products[product] += quantity
                if self.__products[product] <= 0:
                    self.__products.pop(product)
                return True
        raise ProductException("no such product in the Bag")

    def getProducts(self):
        return self.__products


    def getProductQuantity(self, product):
        return self.__products[product]

    def calcSum(self):
        newPrices = self.applyDiscount()
        return sum(newPrices.values())

    def cleanBag(self):
        self.__products = {}

    def printProducts(self):
        products_print = ""
        for product in self.__products:
            products_print += "\n\t\t\tid product:" + str(product.getProductId()) + " name:" + str(
                product.getProductName()) + " quantity:" + str(self.__products.get(product))
        return products_print

    def applyDiscount(self):
        discounts = storePredicateManager.getInstance().getDiscountsByIdStore(self.__storeId)  # brings all of the discounts of the store
        f = lambda discount: discount.getRule().check(self)
        available_discount_values = []
        available_discount = []
        for discount in discounts:
             if f(discount):
                 available_discount_values.append(discount.makeDiscount(self).getDiscount())  # brings us all of the discounts of this bag
                 available_discount.append(discount)

        m = max(available_discount_values)
        g = lambda d: d.makeDiscount(self).getDiscount() >= m
        max_chosen = None
        for available in available_discount:
             if g(available):
                 max_chosen = available
        discount_of_products = max_chosen.getCalc().calcDiscount(self)

        newPrices = {}
        for product in self.__products:
            pId = product.getProductId()
            if pId in discount_of_products.getProducts():
                newPrices[product] = discount_of_products.getProducts()[pId]
        return newPrices





