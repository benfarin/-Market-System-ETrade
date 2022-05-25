from Backend.Business.Rules.DiscountRuleComposite import DiscountRuleComposite
from Backend.Service.DTO.RuleDTO import RuleDTO


class CompositeRuleDTO:

    def __init__(self, rule: DiscountRuleComposite):
        self.__rId = rule.getRuleId()
        self.__rule1 = RuleDTO(rule.getRule1().getRuleId())
        self.__rule2 = RuleDTO(rule.getRule2().getRuleId())

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

    def __str__(self):
        toReturn = "Compsite rule: "
        toReturn += "\n\t rule id: " + str(self.__rId)
        toReturn += "\n\t\t\t" + self.__rule1.__str__()
        toReturn += "\n\t\t\t" + self.__rule2.__str__()
        return toReturn