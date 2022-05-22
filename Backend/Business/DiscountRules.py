from enum import Enum
from Backend.Business.DiscountPackage.StoreDiscount import StoreDiscount
from Backend.Business.DiscountPackage.ProductDiscount import ProductDiscount
from Backend.Business.DiscountPackage.CatagoryDiscount import CataoryDiscount
from Backend.Business.DiscountPackage.Discount import Discount
from Backend.Business.StorePackage.Store import Store
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Business.DiscountPackage.ConditionDiscount import ConditionDiscount
from Backend.Business.Rules.Rule import Rule
from Backend.Business.Rules.ruleCreator import ruleCreator
from Backend.Business.StorePackage.Predicates.StorePredicateManager import storePredicateManager


class ruleContext(Enum):
    store = "store"
    category = "category"
    product = "product"


class ruleType(Enum):
    simple = "simple"
    quantity = "quantity"
    price = "price"
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

    def createConditionalDiscount(self, rId, storeId, discountId, rule_context, rule_type, percent,
                                  catagory, product_id, value_less_than, value_bigger_than):
        discount_calc = self.createCalc(rule_context, percent, catagory, product_id)
        rule = self.createRule(rId, storeId, rule_context, rule_type, catagory, product_id, value_less_than, value_bigger_than)
        return ConditionDiscount(discountId, rule, discount_calc)

    def createRule(self, rId, storeId, discount_type, rule_type, catagory, pid, value_less_than, value_greater_than):
        if rule_type == "price":
            return self.__rules_creator.createStorePriceRule(rId, storeId, value_less_than, value_greater_than)
        if rule_type == "quantity":
            if discount_type == "store":
                return self.__rules_creator.createStoreQuantityRule(rId, storeId, value_less_than, value_greater_than)
            if discount_type == "category":
                return self.__rules_creator.createCategoryRule(rId, storeId, catagory, value_less_than, value_greater_than)
            return self.__rules_creator.createProductRule(rId, storeId, pid, value_less_than, value_greater_than)
        if rule_type == "weight":
            if discount_type == "store":
                return self.__rules_creator.createStoreWeightRule(rId, storeId, value_less_than, value_greater_than)
            return self.__rules_creator.createProductWeightRule(rId, storeId, pid, value_less_than, value_greater_than)

    # def addDiscountOrRule(self, store: Store, discount_id1, discount_id2, original_discount_id):
    #     predicate: storePredicateManager = storePredicateManager.getInstance()
    #     discounts1: Discount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id1)
    #     discount2: Discount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id2)
    #     rule1 = discounts1.getRule()
    #     rule2 = discount2.getRule()
    #     orRule = rule1.OrRule(rule2)
    #     condition_discount = ConditionDiscount(
    #         predicate.getSingleDiscountByID(store.getStoreId(), original_discount_id))
    #     condition_discount.setRule(orRule)
    #     store.addDicount(condition_discount)
    #
    # def addDiscountAndRule(self, store: Store, discount_id1, discount_id2, original_discount_id):
    #     predicate: storePredicateManager = storePredicateManager.getInstance()
    #     discounts1: Discount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id1)
    #     discount2: Discount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id2)
    #     rule1 = discounts1.getRule()
    #     rule2 = discount2.getRule()
    #     andRule = rule1.AddRules(rule2)
    #     condition_discount = ConditionDiscount(
    #         predicate.getSingleDiscountByID(store.getStoreId(), original_discount_id))
    #     condition_discount.setRule(andRule)
    #     store.addDicount(condition_discount)
    #
    # def addDiscountXorRule(self, store: Store, discount_id1, discount_id2, decide):
    #     predicate: storePredicateManager = storePredicateManager.getInstance()
    #     discounts1: ConditionDiscount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id1)
    #     discount2: ConditionDiscount = predicate.getSingleDiscountByID(store.getStoreId(), discount_id2)
    #     xor: ConditionDiscount = discounts1.conditionXOR(discount2, decide)
    #     store.addDicount(xor)
