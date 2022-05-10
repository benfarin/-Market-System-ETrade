from interfaces import IDiscount
from Business.StorePackage import  Bag,Product
from typing import Dict
from Business.DiscountPackage import DiscountCalc, DiscountsOfProducts


class StoreDiscount(IDiscount):

    def __int__(self, percent):
        self.F = lambda a: self.calculate(a, percent)
        self.discountCalc: DiscountCalc = DiscountCalc(self.F)

    def calculate(self, bag: Bag, percent):
        to_return: DiscountsOfProducts = DiscountsOfProducts()
        discount = 0
        products: Dict[Product, int] = bag.getProducts()
        for prod, quantity in products.items():
            discount += quantity*prod.getProductPrice()*percent
            to_return.addProduct(prod.getProductId(),(1-percent)*prod.getProductPrice())
        to_return.increaseDiscount(discount)
        return to_return

    def calcDiscount(self, bag):
        return self.__discountCalc.calcDiscount(bag)

    def max(self, additional_DiscountCal):
        return self.__discountCalc.max(additional_DiscountCal)

    def add(self, discount_calc_2):
        return self.__discountCalc.add(discount_calc_2)
