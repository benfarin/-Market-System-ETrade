import zope

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()


from Backend.Business.Rules.PriceRule import PriceRule
from Backend.Business.Rules.QuantityRule import quantityRule
from Backend.Business.Rules.WeightRule import weightRule
from Backend.Interfaces.IRule import IRule
from ModelsBackend.models import RuleModel


@zope.interface.implementer(IRule)
class PurchaseRuleComposite:

    # rulesTypes: and ,or
    # ruleKind: discountRule , purchaseRule
    def __init__(self, ruleId=None, rule1=None, rule2=None, ruleType=None, ruleKind=None, model=None):
        # self.__ruleId = ruleId
        # self.__ruleKind = ruleKind
        # if rule1.getRuleKind() != ruleKind or rule2.getRuleKind() != ruleKind:
        #     raise Exception("cannot concat between purchase rule and discount rule")
        # self.__rule1: IRule = rule1
        # self.__rule2: IRule = rule2
        # self.__ruleType = ruleType

        if model is None:
            self.__model = RuleModel.objects.get_or_create(ruleID=ruleId, composite_rule_type=ruleType, rule_kind=ruleKind,
                                                           ruleID1=rule1.getModel(), ruleID2=rule2.getModel(),
                                                           rule_class='PurchaseComposite')[0]
            self.__ruleId = ruleId
            self.__rulKind = ruleKind
            if rule1.getRuleKind() != ruleKind or rule2.getRuleKind() != ruleKind:
                raise Exception("cannot concat between purchase rule and discount rule")
            self.__rule1 = rule1
            self.__rule2 = rule2
            self.__ruleType = ruleType
        else:
            self.__model = model
            self.__ruleId = model.ruleID
            self.__rulKind = model.rule_kind
            self.__rule1 = self.__buildRule(model.ruleID1)
            self.__rule2 = self.__buildRule(model.ruleID2)
            if self.__rule1.getRuleKind() != self.__rulKind or self.__rule2.getRuleKind() != self.__rulKind:
                raise Exception("cannot concat between purchase rule and discount rule")
            self.__ruleType = model.composite_rule_type

    def check(self, bag):
        if self.__rule1.getRuleKind() != self.__rule2.getRuleKind():
            raise Exception("cannot concat discount rule and purchase rule")

        if self.__ruleType == 'And':
            return self.__rule1.check(bag) and self.__rule2.check(bag)
        if self.__ruleType == 'Or':
            return self.__rule1.check(bag) or self.__rule2.check(bag)
        else:
            raise Exception("rule type doesn't exist")

    def getRuleId(self):
        return self.__ruleId
        # return self.__model.ruleID

    def getRule1(self):
        return self.__rule1
        # return self.__buildRule(self.__model.ruleID1)

    def getRule2(self):
        return self.__rule2
        # return self.__buildRule(self.__model.ruleID2)

    def getRuleType(self):
        return self.__ruleType
        # return self.__model.composite_rule_type

    def getRuleKind(self):
        return self.__model.rule_kind

    def isComp(self):
        return True

    def removeRule(self):
        self.__rule1.removeRule()
        self.__rule2.removeRule()
        self.__model.delete()

    def __buildRule(self, rule_model):
        if rule_model.rule_class == 'Price':
            return PriceRule(model=rule_model)
        if rule_model.rule_class == 'Quantity':
            return quantityRule(model=rule_model)
        if rule_model.rule_class == 'Weight':
            return weightRule(model=rule_model)
        # if rule_model.rule_class == 'DiscountComposite':
        #     return DiscountRuleComposite(rule_model=rule_model)
        if rule_model.rule_class == 'PurchaseComposite':
            return PurchaseRuleComposite(model=rule_model)
        else:
            raise Exception("cannot concat discount rule and purchase rule")

    def getModel(self):
        return self.__model

    def __eq__(self, other):
        return isinstance(other, PurchaseRuleComposite) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__model.ruleID)
