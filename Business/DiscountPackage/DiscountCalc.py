from Business.StorePackage.Bag import Bag
from interfaces.IDiscount import IDiscount


class DiscountCalc(IDiscount):

    def __init__(self, f):
        self.__F = f

    def calcDiscount(self, bag: Bag):
        return self.__F(bag)

    def max(self, additional_DiscountCal):
        f = lambda bag: self.maxDiscount(bag, additional_DiscountCal, self)
        return DiscountCalc(f)

    def maxDiscount(self, bag: Bag, discount_calc_1: IDiscount, discount_calc_2: IDiscount):
        calc_1 = discount_calc_1.calcDiscount(bag)
        calc_2 = discount_calc_2.calcDiscount(bag)
        if calc_1.getDiscount() < calc_2.getDiscount():
            return calc_2
        return calc_1

    def add(self, additional_DiscountCalc):
        f = lambda bag: self.addDiscount(bag, additional_DiscountCalc, self)
        return DiscountCalc(f)

    def addDiscount(self, bag: Bag,  discount_calc_1: IDiscount, discount_calc_2: IDiscount):
        calc_1 = discount_calc_1.calcDiscount(bag)
        calc_2 = discount_calc_2.calcDiscount(bag)
        discountOfProducts_to_return = calc_1.addDiscount(calc_2.getDiscount, calc_2.getProducts())
        return discountOfProducts_to_return

