from zope.interface import Interface


class IDiscount(Interface):

    def calcDiscount(self, bag):
        pass

    def max(self, additional_DiscountCal):
        pass

    def add(self, discount_calc_2):
        pass
