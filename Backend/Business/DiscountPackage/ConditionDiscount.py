from Backend.Business.Rules.Rule import Rule
from Backend.Business.DiscountPackage.Discount import Discount
from Backend.Business.DiscountPackage.DiscountCalc import DiscountCalc
from Backend.Business.DiscountPackage.DiscountsOfProducts import DiscountOfProducts


class ConditionDiscount(Discount):

    def __init__(self, discountId, rule, discountCalc):
        f = lambda bag: True
        self.__rule = f
        if rule is not None:
            self.__rule = rule
        super().__init__(discountId, discountCalc)

    def setRule(self, rule):
        self.__rule = rule

    def setDefaultRule(self):
        f = lambda bag: True
        self.__rule = f

    def check(self, bag):
        if isinstance(self.__rule, Rule):
            return self.__rule.check(bag)
        return self.__rule(bag)

    def getRule(self):
        return self.__rule

    def acticateDiscount(self, bag):
        if self.__rule.check(bag):
            return self.__calc_discount.calcDiscount(bag)
        return DiscountOfProducts()

    def conditionXOR(self, rule, decide):
        orRule = self.__rule.XorRules(rule, decide)
        self.setRule(orRule)
        return self

    def conditionOR(self, second_rule):
        orRule = self.__rule.OrRules(second_rule)
        self.setRule(orRule)
        return self

    def conditionAND(self, second_rule):
        andRule = self.__rule.AndRules(second_rule)
        self.setRule(andRule)
        return self