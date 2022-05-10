from interfaces import IDiscount
from Business.StorePackage.Product import Product
from Business.StorePackage.Bag import Bag

from typing import Dict
from Business.DiscountPackage.DiscountCalc import DiscountCalc
from Business.DiscountPackage.DiscountsOfProducts import DiscountOfProducts


class CataoryDiscount(IDiscount):

    def __int__(self, catagory, percent):
        self.__F = lambda a: self.calculate(a, catagory, percent)
        self.__discountCalc: DiscountCalc = DiscountCalc(self.__F)

    def calculate(self, bag: Bag, catagory, percent):
        to_return = DiscountOfProducts()
        discount = 0
        products: Dict[Product, int] = bag.getProducts()
        for prod, quantity in products.items():
            if prod.getProductCategory() == catagory:
                discount += quantity*prod.getProductPrice()*percent
                to_return.addProduct(prod.getProductId(), (1-percent)*prod.getProductPrice())
            else:
                to_return.addProduct(prod.getProductId(), prod.getProductPrice())
            to_return.setDiscount(discount)
            return to_return

    def calcDiscount(self, bag):
        return self.__discountCalc.calcDiscount(bag)

    def max(self, additional_DiscountCal):
        return self.__discountCalc.max(additional_DiscountCal)

    def add(self, discount_calc_2):
        return self.__discountCalc.add(discount_calc_2)


