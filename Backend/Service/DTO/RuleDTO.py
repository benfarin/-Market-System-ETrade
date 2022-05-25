class RuleDTO:

    def __init__(self, rId):
        self.__rId = rId


    def getRuleId(self):
        return self.__rId


    def __str__(self):
        toReturn = "Rule: "
        toReturn += "\n\t rule id: " + str(self.__rId)
        return toReturn
