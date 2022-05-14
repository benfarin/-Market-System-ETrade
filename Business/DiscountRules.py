from enum import Enum
from Business.DiscountPackage.StoreDiscount import StoreDiscount
from Business.DiscountPackage.ProductDiscount import ProductDiscount
from Business.DiscountPackage.CatagoryDiscount import CataoryDiscount
from Business.DiscountPackage.Discount import Discount
from Business.StorePackage.Store import Store
from interfaces.IDiscount import IDiscount
from Business.DiscountPackage.ConditionDiscount import ConditionDiscount
from Business.Rules.Rule import Rule
from Business.Rules.ruleCreator import ruleCreator
from Business.StorePackage.Predicates.StorePredicateManager import storePredicateManager


class ruleContext(Enum):
    store = "store"
    category = "category"
    product = "product"


class ruleType(Enum):
    simple = "simple"
    age = "age"
    quantity = "quantity"
    price = "price"
    time = "time"
    weight = "weight"


class DiscountRules:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DiscountRules.__instance is None:
            DiscountRules()
        return DiscountRules.__instance

    def __init__(self):
        self.__rules_creator = ruleCreator()

    def createCalc(self, rulecontext, percent, category, productID):
        if rulecontext == "store":
            return StoreDiscount(percent)
        if rulecontext == "category":
            return CataoryDiscount(category, percent)
        if rulecontext == "product":
            return ProductDiscount(productID, percent)
        raise Exception("not leagal rule contex")

    def createSimpleDiscount(self, discountId, ruleContext, percent, category, productID):
        discount_calc = self.createCalc(ruleContext, percent, category, productID)
        return Discount(discountId, discount_calc)

    def updateDiscount(self, existsDiscount, userId, storeId, ruleContext, discountPercentage, catagory, productId):
        pass

    def removeDiscount(self, discountId):
        pass

    def createConditionalDiscount(self, store: Store, username, store_id, rule_context, rule_type: ruleType, percent,
                                  catagory, product_id, value_less_than, value_bigger_than, time1, time2, discount_id):
        if store is not None:
            discount_calc = self.createCalc(rule_context, percent, catagory, product_id)
            rule = self.createRule(rule_context, rule_type, catagory, product_id, value_less_than, value_bigger_than,
                                   time1, time2)
            conditional_discount = ConditionDiscount(discount_calc)
            conditional_discount.setRule(rule)
            store.addDicount(conditional_discount)

    def createRule(self, discount_type, rule_type, catagory, pid, value_less_than, value_greater_than, time1, time2):
        rule: Rule
        if rule_type == ruleType.age:
            return self.__rules_creator.createUserAgeRule(value_less_than, value_greater_than)
        if rule_type == ruleType.price:
            return self.__rules_creator.createStorePriceRule(value_less_than, value_greater_than)
        if rule_type == ruleType.quantity:
            if discount_type == ruleContext.store:
                return self.__rules_creator.createStorePriceRule(value_less_than, value_greater_than)
            if discount_type == ruleContext.catagory:
                return self.__rules_creator.createCatagoryRule(catagory, value_less_than, value_greater_than)
            return self.__rules_creator.createProductRule(pid, value_less_than, value_greater_than)
        if rule_type == ruleType.weight:
            return self.__rules_creator.createWeightRule(pid, value_less_than, value_greater_than)
        return self.__rules_creator.createTimeRule(time1, time2)

    def addDiscountOrRule(self, store: Store, discount_id1, discount_id2, original_discount_id):
        predicate: storePredicateManager = storePredicateManager.getInstance()
        discounts1: Discount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id1)
        discount2: Discount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id2)
        rule1 = discounts1.getRule()
        rule2 = discount2.getRule()
        orRule = rule1.OrRule(rule2)
        condition_discount = ConditionDiscount(
            predicate.getSingleDiscountByID(store.getStoreId(), original_discount_id))
        condition_discount.setRule(orRule)
        store.addDicount(condition_discount)

    def addDiscountAndRule(self, store: Store, discount_id1, discount_id2, original_discount_id):
        predicate: storePredicateManager = storePredicateManager.getInstance()
        discounts1: Discount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id1)
        discount2: Discount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id2)
        rule1 = discounts1.getRule()
        rule2 = discount2.getRule()
        andRule = rule1.AddRules(rule2)
        condition_discount = ConditionDiscount(
            predicate.getSingleDiscountByID(store.getStoreId(), original_discount_id))
        condition_discount.setRule(andRule)
        store.addDicount(condition_discount)

    def addDiscountXorRule(self, store: Store, discount_id1, discount_id2, decide):
        predicate: storePredicateManager = storePredicateManager.getInstance()
        discounts1: ConditionDiscount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id1)
        discount2: ConditionDiscount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id2)
        xor: ConditionDiscount = discounts1.conditionXOR(discount2, decide)
        store.addDicount(xor)
