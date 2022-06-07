from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount


class simpleDiscountDTO:
    def __init__(self, discount: CategoryDiscount):
        self.__discountId = discount.getDiscountId()
        self.__discountType = discount.getClassType()
        self.__filter = discount.getFilter()
        self.__percent = discount.getDiscountPercent()

    def getDiscountId(self):
        return self.__discountId

    def getDiscountPercent(self):
        return self.__percent

    def setDiscountId(self, newId):
        self.__discountId = newId

    def setDiscountPercent(self, newPercent):
        self.__percent = newPercent

    def strForWeb(self):
        toReturn = self.__discountType + " discount: "
        toReturn += "\n\tdiscount id: " + str(self.__discountId)
        if self.__discountType == 'Category':
            toReturn += "\n\tcategory: " + self.__filter
        elif self.__discountType == 'Product':
            toReturn += "\n\tproduct id: " + str(self.__filter)
        toReturn += "\n\tpercent: " + str(self.__percent)
        return toReturn

    def __str__(self):
        return self.strForWeb()

