from Backend.Interfaces.IRule import IRule


class RuleDTO:

    def __init__(self, rule):
        self.__rId = rule.getRuleId()
        self.__ruleKind = rule.getRuleKind()  # discount / purchase
        self.__ruleType = rule.getRuleType()  # store / category / product
        self.__filter = rule.getRuleFilter()
        self.__atLeast = rule.getAtLeast()
        self._atMost = rule.getAtMost()

    def getRuleId(self):
        return self.__rId

    def strForWeb(self):
        toReturn = self.__ruleKind + " rule " + self.__ruleType + ":"
        toReturn += "\n\trule id: " + str(self.__rId)
        if self.__ruleType == 'Category':
            toReturn += "\n\tcategory: " + self.__filter
        elif self.__ruleType == 'Product':
            toReturn += "\n\tproduct id: " + str(self.__filter)
        toReturn += "\n\tneed at least: " + str(self.__atLeast)
        toReturn += "\n\tcan at most: " + str(self._atMost)
        return toReturn

    def __str__(self):
        return self.strForWeb()
