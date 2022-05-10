import uuid
from Business.DiscountPackage.DiscountCalc import DiscountCalc

class Discount:


    def __init__(self, calc: DiscountCalc):
        self.__id = str(uuid.uuid4())  # unique id
        self.__calc_discount = calc

    def makeDiscount(self, bag):
        return self.__calc_discount.calcDiscount(bag)

