import uuid


class Rule:

    def __init__(self, ruleId, f):
        self.__f = f  # Bag --> bool
        self.__ruleId = ruleId

    def getRuleId(self):
        return self.__ruleId

    def check(self, bag):
        return self.__f(bag)

    def AndRules(self, rule2):
        return lambda bag: self.check(bag) and rule2.check(bag)

    def OrRules(self, rule2):
        return lambda bag: self.check(bag) or rule2.check(bag)

    def XorRules(self, rule2, decide):
        return lambda bag: ((decide == 0 and self.check(bag)) or (decide == 0 and rule2.check(bag)) or False) or \
                           ((decide == 1 and rule2.check(bag)) or (decide == 1 and self.check(bag)) or False)

    def AddRules(self, rule2):
        return lambda bag: self.check(bag) and rule2.check(bag)
