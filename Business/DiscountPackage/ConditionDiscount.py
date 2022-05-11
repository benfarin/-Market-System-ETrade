from Business.Rule import Rule
from Business.DiscountPackage.Discount import Discount
from Business.DiscountPackage.DiscountCalc import DiscountCalc
from Business.DiscountPackage.DiscountsOfProducts import DiscountOfProducts

class ConditionDiscount(Discount):

    def __init__(self,discountCalc:DiscountCalc):
        f = lambda bag: True
        self.__rule = Rule(f)
        super().__init__(discountCalc)


    def setRule(self,rule):
        self.__rule = rule

    def setDefaultRule(self):
        f = lambda bag: True
        self.__rule = Rule(f)

    def getRule(self):
        return self.__rule

    def acticateDiscount(self, bag):
        if self.__rule.check(bag):
            return self.__calc_discount.calcDiscount(bag)
        return DiscountOfProducts()

    def conditionXOR(self, cond, decide):
        f = lambda bag: self.helperXOR(bag, self, cond, decide)
        return ConditionDiscount(DiscountCalc(f))

    def helperXOR(self,bag, cond1, cond2, decide):
        available1 = cond1.getRule(self).check(bag)
        available2= cond1.getRule(self).check(bag)
        if available1 and available2 :
            if decide:
                return cond1.makeDiscount(bag)
            else:
                cond2.makeDiscount(bag)
        else:
            if available1:
                return cond1.makeDiscount(bag)
            else:
                return cond2.acticateDiscount(bag)
    def conditionOR(self, second_rule):
        condition_discount = ConditionDiscount(DiscountCalc(self.__calc_discount))
        orRule =  second_rule.OrRules(self.__rule, second_rule)
        condition_discount.setRule(orRule)
        return condition_discount

    def conditionAND(self, second_rule):
        condition_discount = ConditionDiscount(DiscountCalc(self.__calc_discount))
        orRule = second_rule.AndRules(self.__rule, second_rule)
        condition_discount.setRule(orRule)
        return condition_discount

















