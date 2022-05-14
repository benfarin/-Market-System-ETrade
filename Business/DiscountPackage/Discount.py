import uuid
from Business.DiscountPackage.DiscountCalc import DiscountCalc
from Business.Rules.Rule import Rule


class Discount:

    def __init__(self, discountId, calc):
        self.__id_discount = discountId
        self.__calc_discount = calc

    def makeDiscount(self,
                     bag):  # get some bag and return  an object DisocountOfProduct with all of the products with their id and the percent of discound
        return self.__calc_discount.calcDiscount(bag)

    def getIdDiscount(self):
        return self.__id_discount

    def getRule(self):
        f = lambda bag: True
        rule = Rule(f)
        return rule

    def getCalc(self):
        return self.__calc_discount

