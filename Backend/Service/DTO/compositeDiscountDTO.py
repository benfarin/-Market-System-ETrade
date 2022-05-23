from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Service.DTO.simpleDiscountDTO import simpleDiscountDTO


class compositeDiscountDTO:
    def __init__(self, discount: DiscountComposite):
        self.__discountId = discount.getDiscountId()
        self.__discount1 = simpleDiscountDTO(discount.getDiscount1())
        self.__discount2 = simpleDiscountDTO(discount.getDiscount2())
        self.__discountType = discount.getDiscountType()

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

    def __str__(self):
        toReturn = "Product discount: "
        toReturn += "\n\t discount id: " + str(self.__discountId)
        toReturn += "\n\t\t\t" + self.__discount1.__str__()
        toReturn += "\n\t\t\t" + self.__discount2.__str__()
        toReturn += "\n\tType: " + str(self.__discountType)
        return toReturn
