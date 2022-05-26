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
        self.__model = DiscountModel(discountID=discountId, percent=percent, type='Store')
        self.__model.save()

    def calculate(self, bag):  # return the new price for each product
        # isCheck = self.check(bag)
        newProductPrices: Dict[ProductModel, float] = {}
        products = bag.getProducts()
        for prod in products:
            product = ProductModel.objects.get(product_id=prod.product_ID)
            if product == self.__model.category:
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

    def addSimpleRuleDiscount(self, rule: IRule):
        DiscountRulesModel(discountID=self.__model, ruleID=rule).save()

    def addCompositeRuleDiscount(self, ruleId, rId1, rId2, ruleType, ruleKind):
        r1 = RuleModel.objects.get(ruleID=rId1)
        r2 = RuleModel.objects.get(ruleID=rId2)
        if r1 is None:
            raise Exception("rule1 is not an existing discount")
        if r2 is None:
            raise Exception("rule2 is not an existing discount")
        rule = RuleModel(ruleID=ruleId, rId1=r1, rId2=r2, ruleType=ruleType, ruleKind=ruleKind).save()
        return rule

    def removeDiscountRule(self, rId):
        DiscountRulesModel.objects.get(ruleID=rId).delete()

    def check(self, bag):
        for rule in self.__rules.values():
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
