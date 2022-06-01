import zope

from Backend.Interfaces.IRule import IRule


@zope.interface.implementer(IRule)
class quantityRule:

    # ruleType: store = 1, category = 2, product = 3
    # filerType:  None   , category   ,  productId
    # ruleKind: discountRule = 1 , purchaseRule = 2
    def __init__(self, ruleId, ruleType, filterKey, atLeast, atMost, ruleKind):
        self.__ruleId = ruleId
        self.__ruleKind = ruleKind
        self.__ruleType = ruleType
        self.__filter = filterKey
        self.__atLeast = atLeast
        self.__atMost = atMost

    def check(self, bag):
        s = 0
        for product, quantity in bag.getProducts().items():
            if self.__ruleType == 1:
                s += quantity
            elif self.__ruleType == 2 and product.getProductCategory() == self.__filter:
                s += quantity
            elif self.__ruleType == 3 and product.getProductId() == self.__filter:
                s += quantity
        return self.__atLeast <= s <= self.__atMost

    def getRuleId(self):
        return self.__ruleId

    def getRuleKind(self):
        return self.__ruleKind

