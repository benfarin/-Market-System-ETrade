import zope

from Backend.Interfaces.IRule import IRule
from ModelsBackend.models import RuleModel


@zope.interface.implementer(IRule)
class DiscountRuleComposite:

    # rulesTypes: and = 1, or = 2
    # ruleKind: discountRule = 1 , purchaseRule = 2
    def __init__(self, ruleId, rule1, rule2, ruleType, ruleKind):
        # self.__ruleId = ruleId
        # self.__rulKind = ruleKind
        # if rule1.getRuleKind() != ruleKind or rule2.getRuleKind() != ruleKind:
        #     raise Exception("cannot concat between purchase rule and discount rule")
        # self.__rule1: IRule = rule1
        # self.__rule2: IRule = rule2
        # self.__ruleType = ruleType
        self.__model = RuleModel.objects.get_or_create(ruleID=ruleId, rule_type=ruleType, rule_kind=ruleKind,
                                                       ruleID1=rule1, ruleID2=rule2,  rule_class='DiscountComposite')[0]

    def check(self, bag):
        if self.__model.rule_type == 1:
            return self.__rule1.check(bag) and self.__rule2.check(bag)
        if self.__model.rule_type == 2:
            return self.__rule1.check(bag) or self.__rule2.check(bag)
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

