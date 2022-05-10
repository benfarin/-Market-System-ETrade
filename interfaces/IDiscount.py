from zope.interface import Interface

class IDiscount:

    def calcDiscount(self, bag):
        pass

    def max(self, additional_DiscountCal):
        pass

    def add(self, discount_calc_2):
        pass


