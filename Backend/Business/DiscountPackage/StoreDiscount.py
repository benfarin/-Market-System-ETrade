from typing import Dict
from Backend.Business.StorePackage.Product import Product
from Backend.Interfaces.IDiscount import IDiscount
import zope


@zope.interface.implementer(IDiscount)
class StoreDiscount:

    def __init__(self, discountId, percent):
        self.__discountId = discountId
        self.__percent = percent

    def calculate(self, bag):  # return the new price for each product
        isCheck = self.__check(bag)
        newProductPrices: Dict[Product, float] = {}
        products: Dict[Product, int] = bag.getProducts()  # [product: quantity]
        for prod in products.keys():
            if isCheck:
                newProductPrices[prod] = self.__percent
            else:
                newProductPrices[prod] = prod.getProductPrice()
        return newProductPrices

    def __check(self, bag):
        return True  # we need to add the logic only when we gonna add the rules

    def getDiscountId(self):
        return self.__discountId

    def getDiscountPercent(self):
        return self.__percent
