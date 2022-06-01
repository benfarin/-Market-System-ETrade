from typing import Dict

from Backend.Business.Rules.DiscountRuleComposite import DiscountRuleComposite
from Backend.Business.StorePackage.Product import Product
from Backend.Exceptions.CustomExceptions import NotFoundException
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Interfaces.IRule import IRule
import zope

from ModelsBackend.models import DiscountModel, DiscountRulesModel, RuleModel, ProductModel, ProductsInBagModel


@zope.interface.implementer(IDiscount)
class StoreDiscount:

    def __init__(self, discountId=None, percent=None, model=None):
        # self.__discountId = discountId
        # self.__percent = percent
        # self.__rules: Dict[int: IRule] = {}

        if model is None:
            self.__model = DiscountModel.objects.get_or_create(discountID=discountId, percent=percent, type='Store')[0]
        else:
            self.__model = model

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
        DiscountRulesModel.objects.get_or_create(discountID=self.__model, ruleID=rule.getModel())

    def addCompositeRuleDiscount(self, ruleId, rId1, rId2, ruleType, ruleKind):
        if len(RuleModel.objects.filter(ruleID=rId1)) != 1:
            raise NotFoundException("rule1 is not an existing discount")
        if len(RuleModel.objects.filter(ruleID=rId2)) != 1:
            raise NotFoundException("rule1 is not an existing discount")

        r1 = RuleModel.objects.get(ruleID=rId1)
        r2 = RuleModel.objects.get(ruleID=rId2)

        rule = RuleModel.objects.get_or_create(ruleID=ruleId, ruleID1=r1, ruleID2=r2, composite_rule_type=ruleType,
                                               rule_kind=ruleKind)[0]
        DiscountRulesModel.objects.get_or_create(discountID=self.__model, ruleID=rule)
        DiscountRulesModel.objects.get(discountID=self.__model, ruleID=r1).delete()
        DiscountRulesModel.objects.get(discountID=self.__model, ruleID=r2).delete()
        return DiscountRuleComposite(model=rule)

    def removeDiscountRule(self, rId):
        if len(RuleModel.objects.filter(ruleID=rId)) != 1:
            raise NotFoundException("rule1 is not an existing discount")
        rule = RuleModel.objects.get(ruleID=rId)

        if len(DiscountRulesModel.objects.filter(discountID=self.__model, ruleID=rule)) != 1:
            raise NotFoundException("rule hasn't been connected to any discount")
        DiscountRulesModel.objects.get(discountID=self.__model, ruleID=rule).delete()

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
            totalPrice += (1 - newPrices.get(product)) * product.getProductPrice() * \
                          ProductsInBagModel.objects.get(product_ID=product.getModel(), bag_ID=bag.getModel()).quantity
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

    def __eq__(self, other):
        return isinstance(other, StoreDiscount) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__model.ruleID)

