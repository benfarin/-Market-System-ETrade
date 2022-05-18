class RuleDTO:

    def __init__(self, rId, f):
        self.__rId = rId
        self.__f = f

    def getRuleId(self):
        return self.__rId

    def getRuleFunction(self):
        return self.__f

    def __str__(self):
        toReturn = "Rule: "
        toReturn += "\n\t rule id: " + str(self.__rId)
        return toReturn + "\n\tfunction: " + str(self.__f)
