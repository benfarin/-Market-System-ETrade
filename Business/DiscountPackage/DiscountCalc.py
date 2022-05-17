import zope

from Business.StorePackage.Bag import Bag
from interfaces.IDiscount import IDiscount

@zope.interface.implementer(IDiscount)
class DiscountCalc:

    def __init__(self, f):
        self.__F = f  # f function which get some bag and return DiscountOfProduct which contains all the product (by id as key) and their percent discount on it .

    def calcDiscount(self, bag: Bag):  # get bag and return f(bag)   (= DiscountOfProducts)
        return self.__F(bag)

    def max(self, additional_DiscountCal):
        f = lambda bag: self.maxDiscount(bag, additional_DiscountCal, self)
        return DiscountCalc(f)

    def maxDiscount(self, bag: Bag, discount_calc_1, discount_calc_2):
        calc_1 = discount_calc_1.calcDiscount(bag)
        calc_2 = discount_calc_2.calcDiscount(bag)
        if calc_1.getTotalDiscountPrice() < calc_2.getTotalDiscountPrice():
            return calc_2
        return calc_1

    def add(self, additional_DiscountCalc):
        f = lambda bag: self.addDiscount(bag, self, additional_DiscountCalc)
        return DiscountCalc(f)

    def addDiscount(self, bag: Bag, discount_calc_1, discount_calc_2):
        calc_1 = discount_calc_1.calcDiscount(bag)
        calc_2 = discount_calc_2.calcDiscount(bag)
        # discounts = calc_2.getDiscount()
        products = calc_2.getProducts()
        discountOfProducts_to_return = calc_1.addDiscount(products)
        return discountOfProducts_to_return
