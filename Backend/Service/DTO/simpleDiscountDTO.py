from Backend.Business.DiscountPackage.CategoryDiscount import CategoryDiscount


class simpleDiscountDTO:
    def __init__(self, discount: CategoryDiscount):
            self.__discountId = discount.getDiscountId()
            self.__percent = discount.getPercent()

    def getDiscountId(self):
        return self.__discountId

    def getDiscountPercent(self):
        return self.__percent

    def setDiscountId(self,newId):
        self.__discountId = newId

    def setDiscountPercent(self,newPercent):
        self.__percent = newPercent

    def __str__(self):
        toReturn = "Discount: "
        toReturn += "\n\t discount id: " + str(self.__discountId)
        toReturn += "\n\tpercent: " + str(self.__percent)
        return toReturn