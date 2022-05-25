from zope.interface import Interface


class IRule(Interface):

    def check(self, bag):
        pass

    def getRuleId(self):
        pass

    def getRuleKind(self):
        pass
