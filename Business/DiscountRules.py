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
class DiscountRules:

class ruleContext(Enum):
    store = 'store'
    catagory = 'catagory'
    product = 'product'


class ruleType(Enum):
    simple ='simple'
    age = 'age'
    quantity = 'quantity'
    price = 'price'
    time = 'time'
    weight = 'weight'

class DiscountRules:

    def __init__(self):
        self.__rules_creator = ruleCreator()


    def createCalc(self, rulecontext, percent, catagory, productID):
        discount:IDiscount
        if rulecontext == ruleContext.store  :
            discount = StoreDiscount(percent)
        if rulecontext == ruleContext.catagory  :
            discount = CataoryDiscount(catagory,  percent)
        if rulecontext == ruleContext.product  :
            discount = ProductDiscount(productID, percent)
        return  discount




    def createSimpleDiscount(self, store: Store, discountType: ruleContext,percent, catagory, productID):
        if store is not None:
            discount_calc = self.createSimpleDiscount(discountType, percent, catagory, productID)
            discount = Discount(discount_calc)
            store.addDicount(discount)


    def createConditionalDiscount(self, store:Store, username , store_id, rule_context, rule_type: ruleType, percent, catagory, product_id, value_less_than, value_bigger_than, time1, time2, discount_id ):
        if store is not None:
            discount_calc = self.createCalc(rule_context, percent, catagory, product_id)
            rule = self.createRule(rule_context, rule_type, catagory, product_id, value_less_than, value_bigger_than, time1, time2)
            conditional_discount = ConditionDiscount(discount_calc)
            conditional_discount.setRule(rule)
            store.addDicount(conditional_discount)

    def createRule(self, discount_type, rule_type, catagory, pid, value_less_than, value_greater_than, time1, time2):
        rule: Rule
        if rule_type == ruleType.age:
            return self.__rules_creator.createUserAgeRule(value_less_than,value_greater_than)
        if rule_type == ruleType.price:
            return self.__rules_creator.createStorePriceRule(value_less_than,value_greater_than)
        if rule_type == ruleType.quantity:
            if discount_type == ruleContext.store:
                return self.__rules_creator.createStorePriceRule(value_less_than, value_greater_than)
            if discount_type == ruleContext.catagory:
                return self.__rules_creator.createCatagoryRule(catagory, value_less_than, value_greater_than)
            return self.__rules_creator.createProductRule(pid, value_less_than, value_greater_than)
        if rule_type == ruleType.weight:
            return self.__rules_creator.createWeightRule(pid, value_less_than, value_greater_than)
        return self.__rules_creator.createTimeRule(time1,time2)

    def addDiscountOrRule(self, store: Store, store_id, discount_id1, discount_id2, original_discount_id):
        predicate :storePredicateManager = storePredicateManager.getInstance()
        discounts1 :Discount = predicate.getSingleDiscountByID(store.getStoreId(),discount_id1)
        discount2:Discount = predicate.getSingleDiscountByID(store.getStoreId(),discount_id2)
        rule1 = discounts1.getRule()
        rule2 = discount2.getRule()
        orRule = Rule.OrRule(rule1,rule2)
        condition_discount = ConditionDiscount(predicate.getSingleDiscountByID(store.getStoreId(), original_discount_id))
        condition_discount.setRule(orRule)
        store.addDicount(condition_discount)

    def addDiscountAndRule(self, store: Store,discount_id1, discount_id2, original_discount_id):
        predicate :storePredicateManager = storePredicateManager.getInstance()
        discounts1 :Discount = predicate.getSingleDiscountByID(store.getStoreId(),discount_id1)
        discount2:Discount = predicate.getSingleDiscountByID(store.getStoreId(),discount_id2)
        rule1 = discounts1.getRule()
        rule2 = discount2.getRule()
        andRule = Rule.AddRules(rule1,rule2)
        condition_discount = ConditionDiscount(predicate.getSingleDiscountByID(store.getStoreId(), original_discount_id))
        condition_discount.setRule(andRule)
        store.addDicount(condition_discount)

    def addDiscountXorRule(self, store: Store,discount_id1, discount_id2, decide):
        predicate :storePredicateManager = storePredicateManager.getInstance()
        discounts1 :ConditionDiscount = predicate.getSingleDiscountByID(store.getStoreId(),discount_id1)
        discount2:ConditionDiscount = predicate.getSingleDiscountByID(store.getStoreId(),discount_id2)
        xor : ConditionDiscount= discounts1.conditionXOR(discount2, decide)
        store.addDicount(xor)














