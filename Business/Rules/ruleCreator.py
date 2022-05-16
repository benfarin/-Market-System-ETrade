
from Business.Rules.Rule import Rule
from Business.Managment.UserManagment import UserManagment
from Business.StorePackage.Bag import Bag
from datetime import datetime


class ruleCreator:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ruleCreator.__instance is None:
            ruleCreator()
        return ruleCreator.__instance

    def __init__(self):
        if ruleCreator.__instance is None:
            ruleCreator.__instance = self

    def createProductWeightRule(self, pid, less_than, bigger_than):
        f = lambda bag: self.weightHelper(pid, less_than, bag) and not self.weightHelper(pid, bigger_than, bag)
        return f

    def weightHelper(self, pid, less_than, bag: Bag):
        products = bag.getProducts()
        sum_product_weight = 0
        for prod, quantity in products:
            if prod.getProductId() == pid:
                sum_product_weight += prod.getProductWeight() * quantity
        return sum_product_weight < less_than

    def createProductRule(self, pid, less_than, bigger_than):
        f = lambda bag: self.productRuleHelper(bag, less_than, pid) and not self.productRuleHelper(bag, bigger_than,
                                                                                                   pid)
        return Rule(f)

    def productRuleHelper(self, bag, less_than, pid):
        products = bag.getProducts()
        sum_product = 0
        for prod, quantity in products.items():
            if prod.getProductId() == pid:
                sum_product += quantity
        return sum_product < less_than

    def createStoreTotalPriceLessThanRule(self, less_than, bigger_than):  # return the
        f = lambda bag: self.storeTotalPriceRuleHelper(bag, less_than) and not self.storeTotalPriceRuleHelper(bag,
                                                                                                              bigger_than)
        return f

    def storeTotalPriceRuleHelper(self, bag, less_than):
        products = bag.getProducts()
        sum_product = 0
        for prod, quantity in products:
            sum_product += quantity * prod.getProductPrice()
        return sum_product < less_than

    def createStoreQuantityLessThanRule(self, less_than, bigger_than):  # return the
        f = lambda bag: self.storeQuantityRuleHelper(bag, less_than) and not self.storeQuantityRuleHelper(bag,
                                                                                                          bigger_than)
        return f

    def storeQuantityRuleHelper(self, bag, less_than):
        products = bag.getProducts()
        sum_product = 0
        for prod, quantity in products:
            sum_product += quantity
        return sum_product < less_than

    def createCategoryRule(self, category, less_than, bigger_than):
        f = lambda bag: self.categoryRuleHelper(bag, category, less_than) and not self.categoryRuleHelper(bag, category, bigger_than)
        return f

    def categoryRuleHelper(self, bag, category, less_than):
        products = bag.getProducts()
        sum_product = 0
        for prod, quantity in products:
            if prod.getProductCategory() == category:
                sum_product += quantity
        return sum_product <= less_than

    def createTimeRule(self, time_from, time_to):
        f = lambda bag: self.timeRuleHelper(time_from) and not self.timeRuleHelper(time_to)
        return f

    def timeRuleHelper(self, time_from):
        return time_from < datetime.now()
