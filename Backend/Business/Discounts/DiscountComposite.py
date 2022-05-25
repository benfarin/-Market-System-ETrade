import zope

from Backend.Interfaces.IDiscount import IDiscount


@zope.interface.implementer(IDiscount)
class DiscountComposite:

    # discountTypes: max = 1, add = 2, xor = 3
    def __init__(self, discountId, discount1, discount2, discountType, decide):
        self.__discountId = discountId
        self.__discount1: IDiscount = discount1
        self.__discount2: IDiscount = discount2
        self.__discountType = discountType
        self.__decide = decide

    def calculate(self, bag):
        if self.__discountType == 1:
            totalPrice1 = self.__discount1.getTotalPrice(bag)
            totalPrice2 = self.__discount2.getTotalPrice(bag)
            if totalPrice1 <= totalPrice2:
                return self.__discount1.calculate(bag)
            else:
                return self.__discount2.calculate(bag)
        if self.__discountType == 2:
            calc1 = self.__discount1.calculate(bag)
            calc2 = self.__discount2.calculate(bag)
            newPrices = {}
            for prod in bag.getProducts().keys():
                newPrices[prod] = calc1.get(prod) + calc2.get(prod)
            return newPrices
        if self.__discountType == 3:
            check1 = self.__discount1.check(bag)
            check2 = self.__discount2.check(bag)
            calc1 = self.__discount1.calculate(bag)
            calc2 = self.__discount2.calculate(bag)

            if check1 and not check2:
                return calc1
            if check2 and not check1:
                return calc2
            if check1 and check2:
                if self.__decide == 1:
                    return calc1
                elif self.__decide == 2:
                    return calc2
                else:
                    raise Exception("no such decide number")
            else:
                return self.__discount1.calculate(bag) # doesnt realy matter
        else:
            raise Exception("no such discount type")

    def getDiscountId(self):
        return self.__discountId

    def getDiscount1(self):
        return self.__discount1

    def getDiscount2(self):
        return self.__discount2

    def getDiscountType(self):
        return self.__discountType
