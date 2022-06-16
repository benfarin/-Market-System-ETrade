from typing import Dict

from Backend.Business.Rules.DiscountRuleComposite import DiscountRuleComposite
from Backend.Business.Rules.RuleCreator import RuleCreator
from Backend.Exceptions.CustomExceptions import NotFoundException
from Backend.Interfaces.IDiscount import IDiscount
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
            self.__discountId = discountId
            self.__percent = percent
            self.__rules = {}
        else:
            self.__model = model
            self.__discountId = model.discountID
            self.__percent = model.percent
            self.__rules = {}
            for discountRule in DiscountRulesModel.objects.filter(discountID=self.__model):
                rule = RuleCreator.getInstance().buildRule(discountRule.ruleID)
                self.__rules[rule.getRuleId()] = rule

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
        self.__rules[rule.getRuleId()] = rule

    def addCompositeRuleDiscount(self, ruleId, rId1, rId2, ruleType, ruleKind):
        r1 = self.__rules.get(rId1)
        r2 = self.__rules.get(rId2)

        if r1 is None:
            raise NotFoundException("rule1 is not an existing discount")
        if r2 is None:
            raise NotFoundException("rule1 is not an existing discount")

        # r1 = RuleModel.objects.get(ruleID=rId1)
        # r2 = RuleModel.objects.get(ruleID=rId2)
        ruleModel = RuleModel.objects.get_or_create(ruleID=ruleId, ruleID1=r1.getModel(), ruleID2=r2.getModel(),
                                                    composite_rule_type=ruleType, rule_kind=ruleKind)[0]
        DiscountRulesModel.objects.get_or_create(discountID=self.__model, ruleID=ruleModel)
        DiscountRulesModel.objects.get(discountID=self.__model, ruleID=r1.getModel()).delete()
        DiscountRulesModel.objects.get(discountID=self.__model, ruleID=r2.getModel()).delete()
        self.__rules.pop(rId1)
        self.__rules.pop(rId2)

        rule = DiscountRuleComposite(model=ruleModel)
        self.__rules[ruleId] = rule
        return rule

        # rule = DiscountRuleComposite(ruleId, r1, r2, ruleType, ruleKind)
        # self.__rules[rule.getRuleId()] = rule
        # self.__rules.pop(rId1)
        # self.__rules.pop(rId2)
        # the rule will be only at the rules table, so we can redo him later.

    def removeDiscountRule(self, rId):
        rule = self.__rules.get(rId)

        if rule is None:
            raise NotFoundException("rule1 is not an existing discount")
        # rule = RuleModel.objects.get(ruleID=rId)

        # if len(DiscountRulesModel.objects.filter(discountID=self.__model, ruleID=rule)) != 1:
        #     raise NotFoundException("rule hasn't been connected to any discount")

        DiscountRulesModel.objects.get(discountID=self.__model, ruleID=rule).delete()
        self.__rules.pop(rId)

    def check(self, bag):
        # rules = [RuleCreator.getInstance().buildRule(rule.ruleID)
        #          for rule in DiscountRulesModel.objects.filter(discountID=self.__model.discountID)]
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

    def getAllDiscountRules(self):
        # rules = []
        # for discountRule in DiscountRulesModel.objects.filter(discountID=self.__model):
        #     rule = RuleCreator.getInstance().buildRule(discountRule.ruleID)
        #     rules.append(rule)
        # return rules
        return self.__rules.values()

    def getDiscountId(self):
        return self.__discountId
        # return self.__model.discountID

    def getDiscountPercent(self):
        return self.__percent
        # return self.__model.percent

    def getClassType(self):
        return 'Store'
        # return self.__model.type

    def getFilter(self):
        return None

    def isComp(self):
        return False

    def getModel(self):
        return self.__model

    def remove(self):
        for rule in self.getAllDiscountRules():
            rule.removeRule()
        self.__rules = {}
        self.__model.delete()

    def __eq__(self, other):
        return isinstance(other, StoreDiscount) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__discountId)

