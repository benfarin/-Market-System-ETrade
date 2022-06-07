import zope

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()

from Backend.Interfaces.IRule import IRule
from ModelsBackend.models import RuleModel


@zope.interface.implementer(IRule)
class PriceRule:

    # ruleType: store = 1, category = 2, product = 3
    # filerType:  None   , category   ,  productId
    # ruleKind: discountRule = 1 , purchaseRule = 2
    def __init__(self, ruleId=None, ruleType=None, filterType=None, atLeast=None, atMost=None, ruleKind=None, model=None):
        # self.__ruleId = ruleId
        # self.__ruleKind = ruleKind
        # self.__ruleType = ruleType
        # self.__filterType = filterType
        # self.__atLest = atLeast
        # self.__atMost = atMost
        if model is None:
            self.__model = RuleModel.objects.get_or_create(ruleID=ruleId, simple_rule_type=ruleType, rule_kind=ruleKind, filter_type=filterType,
                                                           at_least=atLeast, at_most=atMost, rule_class='Price')[0]
        else:
            self.__model = model

    def check(self, bag):
        if self.__model.simple_rule_type != 'Store':
            raise Exception("price rule can only be for stores")
        s = 0.0
        for prod, quantity in bag.getProducts().items():
            s += prod.getProductPrice() * quantity
        return self.__model.at_least <= s <= self.__model.at_most

    def getRuleId(self):
        return self.__model.ruleID

    def getRuleKind(self):
        return self.__model.rule_kind

    def getRuleType(self):
        return self.__model.simple_rule_type

    def getRuleFilter(self):
        return self.__model.filter_type

    def getAtLeast(self):
        return self.__model.simple_rule_type

    def getAtMost(self):
        return self.__model.at_most

    def removeRule(self):
        self.__model.delete()

    def isComp(self):
        return False

    def getModel(self):
        return self.__model

    def __eq__(self, other):
        return isinstance(other, PriceRule) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__model.ruleID)
