from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Service.DTO.SimpleDiscountDTO import simpleDiscountDTO


class compositeDiscountDTO:
    def __init__(self, discount: DiscountComposite):
        self.__discountId = discount.getDiscountId()
        if discount.getDiscount1().getClassType() == 'Composite':
            self.__discount1 = compositeDiscountDTO(discount.getDiscount1())
        else:
            self.__discount1 = simpleDiscountDTO(discount.getDiscount1())
        if discount.getDiscount2().getClassType() == 'Composite':
            self.__discount2 = compositeDiscountDTO(discount.getDiscount2())
        else:
            self.__discount2 = simpleDiscountDTO(discount.getDiscount2())
        self.__discountType = discount.getDiscountType()
        self.__decide = discount.getDecide()

    def getDiscountId(self):
        return self.__discountId

    def getDiscount1(self):
        return self.__discount1

    def getDiscount2(self):
        return self.__discount2

    def getDiscountType(self):
        return self.__discountType

    def setDiscountId(self, newId):
        self.__discountId = newId

    def setDiscount1(self, newDiscount1):
        self.__discount1 = newDiscount1

    def setDiscount2(self, newDiscount2):
        self.__discount1 = newDiscount2

    def setDiscountType(self, newType):
        self.__discountType = newType

    def strForWeb(self):
        toReturn = self.__discountType + " discount: "
        toReturn += "\n\tdiscount id: " + str(self.__discountId)
        # toReturn += "\n\t discount1: " + self.__discount1.strForWeb()
        # toReturn += "\n\t discount2: " + self.__discount2.strForWeb()
        toReturn += "\n\tdiscount1: " + str(self.__discount1.getDiscountId())
        toReturn += "\n\tdiscount2: " + str(self.__discount2.getDiscountId())
        if self.__discountType == 'XOR':
            if self.__decide == 1:
                toReturn += "\n\tdecide: first"
            else:
                toReturn += "\n\tdecide: second"
        return toReturn

    def __str__(self):
        return self.strForWeb()
