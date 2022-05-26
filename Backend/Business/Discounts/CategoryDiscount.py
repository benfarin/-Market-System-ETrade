from typing import Dict

import zope

from Backend.Business.Rules.DiscountRuleComposite import DiscountRuleComposite
from Backend.Business.StorePackage.Product import Product
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Interfaces.IRule import IRule
from ModelsBackend.models import DiscountModel, DiscountRulesModel, RuleModel, ProductModel


@zope.interface.implementer(IDiscount)
class CategoryDiscount:

    def __init__(self, discountId, category, percent):
        # self.__discountId = discountId
        # self.__category = category
        # self.__percent = percent
        # self.__rules: Dict[int: IRule] = {}
        self.__model = DiscountModel(discountID=discountId, category=category, percent=percent, type='Category')

    def calculate(self, bag):  # return the new price for each product
        isCheck = self.check(bag)
        newProductPrices: Dict[Product, float] = {}
        products = bag.getProducts()
        for prod in products:
            product = ProductModel.objects.get(product_id=prod.product_ID)
            if product == self.__model.category:
                newProductPrices[prod] = self.__model.percent
            else:
                newProductPrices[prod] = 0
        return newProductPrices
        # newProductPrices: Dict[Product, float] = {}
        # products: Dict[Product, int] = bag.getProducts()  # [product: quantity]
        # for prod in products.keys():
        #     if prod.getProductCategory() == self.__category and isCheck:
        #         newProductPrices[prod] = self.__percent
        #     else:
        #         newProductPrices[prod] = 0
        # return newProductPrices

    def addSimpleRuleDiscount(self, rule):
        DiscountRulesModel(discountID=self.__model, ruleID=rule).save()

    def addCompositeRuleDiscount(self, ruleId, rId1, rId2, ruleType, ruleKind):
        r1 = self.__rules.get(rId1)
        r2 = self.__rules.get(rId2)
        if r1 is None:
            raise Exception("rule1 is not an existing discount")
        if r2 is None:
            raise Exception("rule2 is not an existing discount")
        rule = DiscountRuleComposite(ruleId, r1, r2, ruleType, ruleKind)
        self.__rules[rule.getRuleId()] = rule
        self.__rules.pop(rId1)
        self.__rules.pop(rId2)
        return rule

    def removeDiscountRule(self, rId):
        DiscountRulesModel.objects.get(ruleID=rId).delete()

    def check(self, bag): ###NEED TO EDIT THIS
        for rule in RuleModel.objects.all():
            if not rule.check(bag):
                return False
        return True

    def getTotalPrice(self, bag):
        newPrices = self.calculate(bag)
        totalPrice = 0.0
        for product, quantity in bag.getProducts().items():
            if product.getProductCategory() == self.__category:
                totalPrice += (1 - newPrices.get(product)) * product.getProductPrice() * quantity
            else:
                totalPrice += product.getProductPrice() * quantity
        return totalPrice

    def getDiscountId(self):
        return self.__model.discountID

    def getCategory(self):
        return self.__model.type

    def getDiscountPercent(self):
        return self.__model.percent

