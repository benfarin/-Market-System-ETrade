from typing import Dict

from Backend.Business.Rules.RuleComposite import RuleComposite
from Backend.Business.StorePackage.Product import Product
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Interfaces.IRule import IRule
import zope


@zope.interface.implementer(IDiscount)
class StoreDiscount:

    def __init__(self, discountId, percent):
        self.__discountId = discountId
        self.__percent = percent
        self.__rules: Dict[int: IRule] = {}

    def calculate(self, bag):  # return the new price for each product
        isCheck = self.__check(bag)
        newProductPrices: Dict[Product, float] = {}
        products: Dict[Product, int] = bag.getProducts()  # [product: quantity]
        for prod in products.keys():
            if isCheck:
                newProductPrices[prod] = self.__percent
            else:
                newProductPrices[prod] = 0
        return newProductPrices

    def addSimpleRuleDiscount(self, rule: IRule):
        self.__rules[rule.getRuleId()] = rule

    def addCompositeRuleDiscount(self, ruleId, rId1, rId2, ruleType):
        r1 = self.__discounts.get(rId1)
        r2 = self.__discounts.get(rId2)
        if r1 is None:
            raise Exception("rule1 is not an existing discount")
        if r2 is None:
            raise Exception("rule2 is not an existing discount")
        rule = RuleComposite(ruleId, r1, r2, ruleType)
        self.__rules[rule.getRuleId()] = rule
        self.__rules.pop(rId1)
        self.__rules.pop(rId2)
        return rule

    def removeDiscountRule(self, rId):
        self.__rules.pop(rId)

    def __check(self, bag):
        for rule in self.__rules.values():
            if not rule.check(bag):
                return False
        return True

    def getTotalPrice(self, bag):
        newPrices = self.calculate(bag)
        totalPrice = 0.0
        for product, quantity in bag.getProducts().items():
            totalPrice += (1 - newPrices.get(product)) * product.getProductPrice() * quantity
        return totalPrice

    def getDiscountId(self):
        return self.__discountId

    def getDiscountPercent(self):
        return self.__percent
