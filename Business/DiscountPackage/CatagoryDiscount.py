import zope

from interfaces.IDiscount import IDiscount
from Business.StorePackage.Product import Product
from Business.StorePackage.Bag import Bag

from typing import Dict
from Business.DiscountPackage.DiscountCalc import DiscountCalc
from Business.DiscountPackage.DiscountsOfProducts import DiscountOfProducts


@zope.interface.implementer(IDiscount)
class CataoryDiscount:

    def __init__(self, category, percent):
        self.__F = lambda a: self.calculate(a, category, percent)
        self.__discountCalc = DiscountCalc(self.__F)

    def calculate(self, bag, category, percent):  # (bag,catagory,percent) --> DiscountOfProducts which contain all of the product which answer on the catagory, the products is calaculated after the discount and held the price after discount <pid,price>
        to_return = DiscountOfProducts()
        # discount = 0
        products: Dict[Product, int] = bag.getProducts()
        for prod, quantity in products.items():
            if prod.getProductCategory() == category:
                # discount += percent
                to_return.addProduct(prod, 1 - percent)
            else:
                to_return.addProduct(prod, 1.0)
            # to_return.setDiscount(discount)
        return to_return

    def calcDiscount(self, bag):
        return self.__discountCalc.calcDiscount(bag)

    def max(self, additional_DiscountCal):
        return self.__discountCalc.max(additional_DiscountCal)

    def add(self, discount_calc_2):
        return self.__discountCalc.add(discount_calc_2)
