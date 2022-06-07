class RuleDTO:

    def __init__(self, rule):
        self.__rId = rule.getRuleId()

    def getRuleId(self):
        return self.__rId

    def __str__(self):
        toReturn = "Rule: "
        toReturn += "\n\t rule id: " + str(self.__rId)
        return toReturn
