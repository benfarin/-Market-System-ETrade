import zope

from Backend.Interfaces.IRule import IRule


@zope.interface.implementer(IRule)
class weightRule:

    # ruleType: store = 1, category = 2, product = 3
    # filerType:  None   , category   ,  productId
    def __init__(self, ruleId, ruleType, filterKey, atLeast, atMost):
        self.__ruleId = ruleId
        self.__ruleType = ruleType
        self.__filter = filterKey
        self.__atLest = atLeast
        self.__atMost = atMost

    def check(self, bag):
        s = 0
        for product, quantity in bag.getProducts().items():
            if self.__ruleType == 1:
                s += product.getProductWeight() * quantity
            elif self.__ruleType == 2 and product.getProductCategory() == self.__filter:
                s += product.getProductWeight() * quantity
            elif self.__ruleType == 3 and product.getProductId() == self.__filter:
                s += product.getProductWeight() * quantity
        return self.__atLest <= s <= self.__atMost

    def getRuleId(self):
        return self.__ruleId
