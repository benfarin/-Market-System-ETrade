import zope

from Backend.Interfaces.IRule import IRule


@zope.interface.implementer(IRule)
class weightRule:

    # ruleType: store = 1, category = 2, product = 3
    # filerType:  None   , category   ,  productId
    # ruleKind: discountRule = 1 , purchaseRule = 2
    def __init__(self, ruleId, ruleType, filterKey, atLeast, atMost, ruleKind):
        self.__ruleId = ruleId
        self.__ruleKind = ruleKind
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

    def getRuleKind(self):
        return self.__ruleKind
