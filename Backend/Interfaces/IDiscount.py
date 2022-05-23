from zope.interface import Interface


class IDiscount(Interface):

    def calculate(self, bag):
        pass

    def addSimpleRuleDiscount(self, rule):
        pass

    def addCompositeRuleDiscount(self, ruleId, rId1, rId2, ruleType):
        pass

    def removeDiscountRule(self, rId):
        pass

    def getTotalPrice(self, bag):
        pass

    def getDiscountId(self):
        pass
