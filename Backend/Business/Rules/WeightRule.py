import zope

from Backend.Interfaces.IRule import IRule
from ModelsBackend.models import RuleModel


@zope.interface.implementer(IRule)
class weightRule:

    # ruleType: store = 1, category = 2, product = 3
    # filerType:  None   , category   ,  productId
    # ruleKind: discountRule = 1 , purchaseRule = 2
    def __init__(self, ruleId=None, ruleType=None, filterKey=None, atLeast=None, atMost=None, ruleKind=None,
                 model=None):
        # self.__ruleId = ruleId
        # self.__ruleKind = ruleKind
        # self.__ruleType = ruleType
        # self.__filter = filterKey
        # self.__atLest = atLeast
        # self.__atMost = atMost
        if model is None:
            self.__model = RuleModel.objects.get_or_create(ruleID=ruleId, simple_rule_type=ruleType, rule_kind=ruleKind,
                                                           filter_type=filterKey,
                                                           at_least=atLeast, at_most=atMost, rule_class='Weight')[0]
        else:
            self.__model = model

    def check(self, bag):
        s = 0
        for prod in bag.getProducts():
            if self.simple_rule_type == 'Store':
                s += prod.product_ID.weight * prod.quantity
            elif self.simple_rule_type == 'Category' and prod.product_ID.category == self.__model.filter_type:
                s += prod.product_ID.weight * prod.quantity
            elif self.simple_rule_type == 'Product' and prod.product_ID.product_id == self.__model.filter_type:
                s += prod.product_ID.weight * prod.quantity
        return self.__atLest <= s <= self.__atMost

    def getRuleId(self):
        return self.__model.ruleID

    def getRuleKind(self):
        return self.__model.rule_kind
