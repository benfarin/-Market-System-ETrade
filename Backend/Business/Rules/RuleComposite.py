import zope

from Backend.Interfaces.IRule import IRule


@zope.interface.implementer(IRule)
class RuleComposite:

    # rulesTypes: and = 1, or = 2, xor = 3, cond = 4
    def __init__(self, ruleId, rule1, rule2, ruleType):
        self.__ruleId = ruleId
        self.__rule1: IRule = rule1
        self.__rule2: IRule = rule2
        self.__ruleType = ruleType

    def check(self, bag):
        if self.__ruleType == 1:
            return self.__rule1.check(bag) and self.__rule2.check(bag)
        if self.__ruleType == 2:
            return self.__rule1.check(bag) or self.__rule2.check(bag)
        # if self.__ruleType == 4:
        #     return self.__rule1.check(bag)  # rule 2 will be None
        else:
            raise Exception("rule type doesn't exist")

    def getRuleId(self):
        return self.__ruleId

    def getRule1(self):
        return self.__rule1

    def getRule2(self):
        return self.__rule2

    def getRuleType(self):
        return self.__ruleType
