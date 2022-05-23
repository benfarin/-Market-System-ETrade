from typing import Dict

import zope

from Backend.Business.StorePackage.Product import Product
from Backend.Interfaces.IDiscount import IDiscount


@zope.interface.implementer(IDiscount)
class ProductDiscount:

    def __init__(self, discountId, productId, percent):
        self.__discountId = discountId
        self.__productId = productId
        self.__percent = percent

    def calculate(self, bag):  # return the new price for each product
        isCheck = self.__check(bag)
        newProductPrices: Dict[Product, float] = {}
        products: Dict[Product, int] = bag.getProducts()  # [product: quantity]
        for prod in products.keys():
            if prod.getProductId() == self.__productId and isCheck:
                newProductPrices[prod] = self.__percent
            else:
                newProductPrices[prod] = 0
        return newProductPrices

    def __check(self, bag):
        return True  # we need to add the logic only when we gonna add the rules

    def getTotalPrice(self, bag):
        newPrices = self.calculate(bag)
        totalPrice = 0.0
        for product, quantity in bag.getProducts().items():
            if product.getProductId() == self.__productId:
                totalPrice += (1 - newPrices.get(product)) * product.getProductPrice() * quantity
            else:
                totalPrice += product.getProductPrice() * quantity
        return totalPrice

    def getDiscountId(self):
        return self.__discountId

    def getProductId(self):
        return self.__productId

    def getDiscountPercent(self):
        return self.__percent
