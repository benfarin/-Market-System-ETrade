import zope

from Backend.Interfaces.IRule import IRule


@zope.interface.implementer(IRule)
class PriceRule:

    # ruleType: store = 1, category = 2, product = 3
    # filerType:  None   , category   ,  productId
    # ruleKind: discountRule = 1 , purchaseRule = 2
    def __init__(self, ruleId, ruleType, filterType, atLeast, atMost, ruleKind):
        self.__ruleId = ruleId
        self.__ruleKind = ruleKind
        self.__ruleType = ruleType
        self.__filterType = filterType
        self.__atLest = atLeast
        self.__atMost = atMost

    def check(self, bag):
        if self.__ruleType != 1:
            raise Exception("price rule can only be for stores")
        s = 0.0
        for product, quantity in bag.getProducts().items():
            s += product.getProductPrice() * quantity
        return self.__atLest <= s <= self.__atMost

    def getRuleId(self):
        return self.__ruleId

    def getRuleKind(self):
        return self.__ruleKind
