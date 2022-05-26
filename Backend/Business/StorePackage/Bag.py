import zope
from zope.interface import implements

import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()

from Backend.Exceptions.CustomExceptions import QuantityException, ProductException
from Backend.Interfaces.IBag import IBag
from ModelsBackend.models import BagModel, ProductsInBagModel, ProductModel


@zope.interface.implementer(IBag)
class Bag:

    def __init__(self, storeId):
        # self.__storeId = storeId
        # self.__products = {}  # product : quantity
        self.__b = BagModel(storeId=storeId)
        self.__b.save()

    def getStore(self):
        pass

    def isEmpty(self):
        return not BagModel.objects.filter(products__bagmodel=self.__b).exists()

    def getStoreId(self):
        return self.__b.storeId

    def getBag(self):
        return self

    def addProduct(self, product, quantity):
        if quantity <= 0:
            raise QuantityException("cannot add negative quantity of product")
        if ProductsInBagModel.objects.filter(product_ID=product, quantity=quantity):
            ProductsInBagModel(bag=self.__b, product_ID=product, quantity=quantity)
            return True
        ProductsInBagModel.objects.get(bag=self.__b, product=product).quantity += quantity
        return True

    def removeProduct(self, productId):
        for product in ProductsInBagModel.objects.filter(bag=self.__b):
            if product.product_ID == productId:
                quantity = product.quantity
                ProductsInBagModel.objects.get(bag=self.__b, product_ID=product, quantity=quantity)
                return quantity
        raise ProductException("no such product in the Bag")

    def updateBag(self, productId, quantity):
        for product in ProductsInBagModel.objects.filter(bag=self.__b):
            if product.product_ID == productId:
                product.quantity += quantity
                if product.quantity < 0:
                    ProductsInBagModel.objects.get(bag=self.__b, product_ID=product, quantity=quantity).delete()
                return True
        raise ProductException("no such product in the Bag")

    def getProducts(self):
        return ProductsInBagModel.objects.filter(bag=self.__b)

    def addBag(self, bag):
        for product in ProductsInBagModel.objects.filter(bag=bag):
            if product in ProductsInBagModel.objects.filter(bag=self.__b):
                ProductsInBagModel.objects.get(bag=self.__b, product_ID=product).quantity +=\
                    ProductsInBagModel.objects.get(bag=bag, product_ID=product).quantity
            else:
                ProductsInBagModel.objects.get(bag=self.__b, product_ID=product).quantity = \
                    ProductsInBagModel.objects.get(bag=bag, product_ID=product).quantity
        return True

    def getProductQuantity(self, product):
        return ProductsInBagModel.objects.filter(bag=self.__b, product_ID=product)

    def calcSum(self, discounts):  ###NEED TO CHANGE
        return self.applyDiscount(discounts)

    def cleanBag(self):
        ProductsInBagModel.objects.filter(bag=self.__b).delete()

    def printProducts(self):
        products_print = ""
        for product in ProductsInBagModel.objects.filter(bag=self.__b):
            products_print += "\n\t\t\tid product:" + str(product.product_ID) + " name:" + str(
                ProductModel.objects.get(product_id=product).name) + " quantity:" + str(product.quantity)
        return products_print

    def __searchProductByProductId(self, pId):
        for product in ProductsInBagModel.objects.filter(bag=self.__b):
            if product.product_ID == pId:
                return product
        return None

    def applyDiscount(self, discounts): ###NEED TO ADD THIS
        if discounts is None or discounts == {}:
            return self.calc()
        minPrice = float('inf')
        for discount in discounts.values():
            newPrice = self.calcWithDiscount(discount.calculate(self))
            if newPrice < minPrice:
                minPrice = newPrice
        if minPrice < float('inf'):
            return minPrice
        else:
            return self.calc()

    def calcWithDiscount(self, discount_of_product): ###NEED TO CHANGE THAT
        s = 0
        for prod in discount_of_product.keys():
            s += (1 - discount_of_product[prod]) * prod.getProductPrice() * self.__products.get(prod)
        return s

    def calc(self):
        s = 0.0
        for product in ProductsInBagModel.objects.filter(bag=self.__b):
            s += ProductModel.objects.get(product_id=product) * ProductsInBagModel.objects.get(bag_ID=self.__b,
                                                                                               product_ID=product).quantity
        return s





