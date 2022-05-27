import zope

from Backend.Interfaces.IRule import IRule
from ModelsBackend.models import RuleModel

import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()

@zope.interface.implementer(IRule)
class PriceRule:

    # ruleType: store = 1, category = 2, product = 3
    # filerType:  None   , category   ,  productId
    # ruleKind: discountRule = 1 , purchaseRule = 2
    def __init__(self, ruleId, ruleType, filterType, atLeast, atMost, ruleKind):
        # self.__ruleId = ruleId
        # self.__ruleKind = ruleKind
        # self.__ruleType = ruleType
        # self.__filterType = filterType
        # self.__atLest = atLeast
        # self.__atMost = atMost
        self.__model = RuleModel.objects.get_or_create(ruleID=ruleId, rule_type=ruleType, rule_kind=ruleKind, filter_type=filterType,
                                 at_least=atLeast, at_most=atMost, rule_class='Price')[0]

    def check(self, bag):
        if self.__model.rule_type != 'Store':
            raise Exception("price rule can only be for stores")
        s = 0.0
        for prod in bag.getProducts():
            product = prod.product_ID
            s += product.price * prod.quantity
        return self.__model.at_least <= s <= self.__model.at_most

    def getRuleId(self):
        return self.__model.ruleID

    def getRuleKind(self):
        return self.__model.rule_kind
