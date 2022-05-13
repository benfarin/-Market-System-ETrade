import uuid

class Rule:

    def __init__(self, f):
        self.__f = f  # Bag --> bool
        self.__id = str(uuid.uuid4())

    def check(self, bag):
        return self.__f(bag)

    def AndRules(self, rule2):
        return lambda bag: self.check(bag) and rule2.check(bag)

    def OrRules(self, rule2):
        return lambda bag: self.check(bag) or rule2.check(bag)

    def OrRule(self, rule1, rule2):
        return lambda bag: rule1.check(bag) or rule2.check(bag)

    def AddRules(self, rule1, rule2):
        return lambda bag: rule1.check(bag) and rule2.check(bag)
