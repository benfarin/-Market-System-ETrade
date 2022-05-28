import zope

from Backend.Business.Rules.PriceRule import PriceRule
from Backend.Business.Rules.QuantityRule import quantityRule
from Backend.Business.Rules.WeightRule import weightRule
from Backend.Interfaces.IRule import IRule
from ModelsBackend.models import RuleModel


@zope.interface.implementer(IRule)
class PurchaseRuleComposite:

    # rulesTypes: and = 1, or = 2
    # ruleKind: discountRule = 1 , purchaseRule = 2
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
                                                           ruleID1=rule1, ruleID2=rule2,  rule_class='PurchaseComposite')[0]
        else:
            self.__model = model

    def check(self, bag):
        rule1 = self.__buildRule(self.__model.ruleID1)
        rule2 = self.__buildRule(self.__model.ruleID2)
        if rule1.getRuleKind() != rule2.getRuleKind():
            raise Exception("cannot concat discount rule and purchase rule")

        if self.__ruleType == 'And':
            return rule1.check(bag) and rule2.check(bag)
        if self.__ruleType == 'Or':
            return rule1.check(bag) or rule2.check(bag)
        else:
            raise Exception("rule type doesn't exist")

    def getRuleId(self):
        return self.__model.ruleID

    def getRule1(self):
        return self.__model.ruleID1

    def getRule2(self):
        return self.__model.ruleID2

    def getRuleType(self):
        return self.__model.rule_type

    def getRuleKind(self):
        return self.__model.rule_kind

    def __buildRule(self, rule_model):
        if rule_model.rule_class == 'Price':
            return PriceRule(rule_model=rule_model)
        if rule_model.rule_class == 'Quantity':
            return quantityRule(rule_model=rule_model)
        if rule_model.rule_class == 'Weight':
            return weightRule(rule_model=rule_model)
        # if rule_model.rule_class == 'DiscountComposite':
        #     return DiscountRuleComposite(rule_model=rule_model)
        if rule_model.rule_class == 'PurchaseComposite':
            return PurchaseRuleComposite(rule_model=rule_model)
        else:
            raise Exception("cannot concat discount rule and purchase rule")
