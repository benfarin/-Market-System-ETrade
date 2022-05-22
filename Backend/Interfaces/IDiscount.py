from zope.interface import Interface


class IDiscount(Interface):

    def calculate(self, bag):
        pass

    def getTotalPrice(self, bag):
        pass

    def getDiscountId(self):
        pass
