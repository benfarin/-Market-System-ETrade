from typing import Dict

from Backend.Business.Rules.DiscountRuleComposite import DiscountRuleComposite
from Backend.Business.StorePackage.Product import Product
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Interfaces.IRule import IRule
import zope

from ModelsBackend.models import DiscountModel, DiscountRulesModel, RuleModel, ProductModel, ProductsInBagModel


@zope.interface.implementer(IDiscount)
class StoreDiscount:

    def __init__(self, discountId, percent):
        # self.__discountId = discountId
        # self.__percent = percent
        # self.__rules: Dict[int: IRule] = {}
        self.__model = DiscountModel.objects.get_or_create(discountID=discountId, percent=percent, type='Store')[0]

    def calculate(self, bag):  # return the new price for each product
        isCheck = self.check(bag)
        newProductPrices: Dict[ProductModel, float] = {}
        products = bag.getProducts()
        for prod in products:
            if isCheck:
                newProductPrices[prod] = self.__model.percent
            else:
                newProductPrices[prod] = 0
        return newProductPrices

        # isCheck = self.check(bag)
        # newProductPrices: Dict[Product, float] = {}
        # products: Dict[Product, int] = bag.getProducts()  # [product: quantity]
        # for prod in products.keys():
        #     if isCheck:
        #         newProductPrices[prod] = self.__percent
        #     else:
        #         newProductPrices[prod] = 0
        # return newProductPrices

    def addSimpleRuleDiscount(self, rule):
        DiscountRulesModel.objects.get_or_create(discountID=self.__model, ruleID=rule)[0]

    def addCompositeRuleDiscount(self, ruleId, rId1, rId2, ruleType, ruleKind):
        r1 = RuleModel.objects.get(ruleID=rId1)
        r2 = RuleModel.objects.get(ruleID=rId2)
        if r1 is None:
            raise Exception("rule1 is not an existing discount")
        if r2 is None:
            raise Exception("rule2 is not an existing discount")
        rule = RuleModel(ruleID=ruleId, rId1=r1, rId2=r2, ruleType=ruleType, ruleKind=ruleKind).save()
        self.addSimpleRuleDiscount(rule)
        self.removeDiscountRule(r1.ruleID)
        self.removeDiscountRule(r2.ruleID)
        return rule

    def removeDiscountRule(self, rId):
        DiscountRulesModel.objects.get(ruleID=rId).delete()

    def check(self, bag):
        rules = [rule.ruleID for rule in DiscountRulesModel.objects.filter(discountID=self.__model.discountID)]
        for rule in rules:
            if not rule.check(bag):
                return False
        return True

    def getTotalPrice(self, bag):
        newPrices = self.calculate(bag)
        totalPrice = 0.0
        for product in bag.getProducts():
            totalPrice += (1 - newPrices.get(product)) * product.price * \
                          ProductsInBagModel.objects.get(product_ID=product, bag=bag).quantity
        return totalPrice

        # newPrices = self.calculate(bag)
        # totalPrice = 0.0
        # for product, quantity in bag.getProducts().items():
        #     totalPrice += (1 - newPrices.get(product)) * product.getProductPrice() * quantity
        # return totalPrice


    def getDiscountId(self):
        return self.__model.discountID

    def getDiscountPercent(self):
        return self.__model.percent

    def getModel(self):
        return self.__model

    def remove(self):
        self.__model.delete()
