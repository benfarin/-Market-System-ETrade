from Backend.Business.Rules.DiscountRuleComposite import DiscountRuleComposite
from Backend.Service.DTO.RuleDTO import RuleDTO


class CompositeRuleDTO:

    def __init__(self, rule: DiscountRuleComposite):
        self.__rId = rule.getRuleId()
        self.__ruleKind = rule.getRuleKind()
        rule1Type = rule.getRule1().getRuleType()
        if rule1Type == 'Or' or rule1Type == 'And':
            self.__rule1 = CompositeRuleDTO(rule.getRule1())
        else:
            self.__rule1 = RuleDTO(rule.getRule1())
        rule2Type = rule.getRule1().getRuleType()
        if rule2Type == 'Or' or rule2Type == 'And':
            self.__rule2 = CompositeRuleDTO(rule.getRule2())
        else:
            self.__rule2 = RuleDTO(rule.getRule2())
        self.__ruleType = rule.getRuleType()

    def getRuleId(self):
        return self.__rId

    def getRule1(self):
        return self.__rule1

    def getRule2(self):
        return self.__rule2

    def setRuleId(self,newId):
        self.__rId = newId

    def setRule1(self, rule1):
        self.__rule1 = rule1

    def setRule2(self, rule2):
        self.__rule2 = rule2

    def strForWeb(self):
        toReturn = self.__ruleKind + " rule for " + self.__ruleType + ":"
        toReturn += "\n\trule id: " + str(self.__rId)
        # toReturn += "\n\trule1: " + self.__rule1.strForWeb()
        # toReturn += "\n\trule2: " + self.__rule2.strForWeb()
        toReturn += "\n\trule1: " + str(self.__rule1.getRuleId())
        toReturn += "\n\trule2: " + str(self.__rule2.getRuleId())
        return toReturn

    def __str__(self):
        return self.strForWeb()
