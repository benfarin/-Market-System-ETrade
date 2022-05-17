import zope
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge
from AcceptanceTests.Bridges.MarketBridge import MarketRealBridge
from Business.Rules.ruleCreator import ruleCreator

@zope.interface.implementer(IMarketBridge)
class MarketProxyBridge:
    def __init__(self, real_subject: MarketRealBridge):
        self._real_subject = real_subject

    def request(self) -> bool:
        if self.check_access():
            self._real_subject.request()
        else:
            return True

    def check_access(self) -> bool:
        return self._real_subject is None

    def add_product_to_store(self, store_id, user_id, name, price, category, weight, key_words):
        if self.check_access():
            return True
        else:
            return self._real_subject.add_product_to_store(store_id, user_id, name, price, category, weight, key_words)

    def remove_product_from_store(self, store_id, user_id, prod_id):
        if self.check_access():
            if store_id < 0 or prod_id < 0 or prod_id < 0:
                return False
            return True
        return self._real_subject.remove_product_from_store(store_id, user_id, prod_id)

    def edit_product_price(self, store_id, user_id, prod_id, new_price):
        if self.check_access():
            if new_price < 0 or store_id < 0 or prod_id < 0:
                return False
            return True
        return self._real_subject.edit_product_price(store_id, user_id, prod_id, new_price)

    def search_product_category(self, category):
        if self.check_access():
            return True
        return self._real_subject.search_product_category(category)

    def search_product_name(self, product_name):
        if self.check_access():
            return True
        return self._real_subject.search_product_name(product_name)

    def add_quantity_to_store(self, store_id, user_id, productID, quantity):
        if self.check_access():
            return True
        return self._real_subject.add_quantity_to_store(store_id, user_id, productID, quantity)

    def search_product_keyWord(self, key_word):
        if self.check_access():
            return True
        return self._real_subject.search_product_keyWord(key_word)

    def search_product_price_range(self, price_min, price_max):
        if self.check_access():
            return True
        return self._real_subject.search_product_price_range(price_min, price_max)

    def appoint_store_owner(self, store_id, assigner_id, assignee_id):
        if self.check_access():
            return True
        return self._real_subject.appoint_store_owner(store_id, assigner_id, assignee_id)

    def appoint_store_manager(self, store_id, assigner_id, assignee_id):
        if self.check_access():
            return True
        return self._real_subject.appoint_store_manager(store_id, assigner_id, assignee_id)

    def set_stock_manager_perm(self, store_id, assigner_id, assignee_id):
        if self.check_access():
            return True
        return self._real_subject.set_stock_manager_perm(store_id, assigner_id, assignee_id)

    def set_change_perm(self, store_id, assigner_id, assignee_id):
        if self.check_access():
            return True
        return self._real_subject.set_change_perm(store_id, assigner_id, assignee_id)

    def close_store(self, store_id, user_id):
        if self.check_access():
            return True
        return self._real_subject.close_store(store_id, user_id)

    def get_store_info(self, store_id, user_id):
        if self.check_access():
            if store_id < 0:
                return False
            return True
        return self._real_subject.get_store_info(store_id, user_id)

    def get_cart_info(self, user_id):
        if self.check_access():
            return True
        return self._real_subject.get_cart_info(user_id)

    def edit_product_name(self, user_id, store_id, prod_id, new_name):
        if self.check_access():
            return True
        return self._real_subject.edit_product_name(user_id, store_id, prod_id, new_name)

    def edit_product_category(self, user_id, store_id, prod_id, new_category):
        if self.check_access():
            return True
        return self._real_subject.edit_product_category(user_id, store_id, prod_id, new_category)

    def edit_product_Weight(self, user_id, store_id, prod_id, new_weight):
        if self.check_access():
            return True
        return self._real_subject.edit_product_Weight(user_id, store_id, prod_id, new_weight)

    def get_cart(self, user_id):
        if self.check_access():
            return True
        return self._real_subject.get_cart(user_id)

    def get_store_by_ID(self, store_id):
        if self.check_access():
            return True
        return self._real_subject.get_store(store_id)

    def getAllStores(self):
        if self.check_access():
            return True
        return self._real_subject.getAllStores()

    def getUserStore(self, userId):
        if self.check_access():
            return True
        return self._real_subject.getUserStore(userId)

    def print_purchase_history(self, store_id, user_id):
        if self.check_access():
            return True
        return self._real_subject.print_purchase_history(store_id, user_id)

    def addSimpleDiscount_Store(self, userId, storeId, precent):
        if self.check_access():
            return True
        return self._real_subject.addSimpleDiscount_Store(userId, storeId, precent)

    def addSimpleConditionDiscount_Store(self, userId, storeId, condition, precent, fromVal, toVal):
        if self.check_access():
            return True
        return self._real_subject.addSimpleConditionDiscount_Store(userId, storeId, condition, precent, fromVal, toVal)

    def addSimpleDiscount_Category(self, userId, storeId, precent, category):
        if self.check_access():
            return True
        return self._real_subject.addSimpleDiscount_Category(userId, storeId, precent, category)

    def addSimpleConditionDiscount_Category(self, userId, storeId, precent, condition, category, fromVal, toVal):
        if self.check_access():
            return True
        return self._real_subject.addSimpleConditionDiscount_Category(userId, storeId, precent, condition, category, fromVal, toVal)

    def addSimpleDiscount_Product(self, userId, storeId, precent, productId):
        if self.check_access():
            return True
        return self._real_subject.addSimpleDiscount_Product(userId, storeId, precent, productId)

    def addSimpleConditionDiscount_Product(self, userId, storeId, precent, condition, productId, fromVal, toVal):
        if self.check_access():
            return True
        return self._real_subject.addSimpleConditionDiscount_Product(userId, storeId, precent, condition, productId, fromVal, toVal)

    def addConditionDiscountAdd(self, userId, storeId, dId1, dId2):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountAdd(userId, storeId, dId1, dId2)

    def addConditionDiscountMax(self, userId, storeId, dId1, dId2):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountMax(userId, storeId, dId1, dId2)

    def addConditionDiscountXor(self, userId, storeId,  dId, pred1, pred2, decide):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountXor(userId, storeId, dId, pred1, pred2, decide)

    def addConditionDiscountAnd(self, userId, storeId, dId, pred1, pred2):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountAnd(userId, storeId,  dId, pred1, pred2)

    def addConditionDiscountOr(self, userId, storeId, dId, pred1, pred2):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountOr(userId, storeId, dId, pred1, pred2)

    def createProductWeightRule(self,uid,pid, less_than, more_than):
        if self.check_access():
            return True
        return self._real_subject.createProductWeightRule(uid ,pid, less_than, more_than)

    def removeDiscount(self,  userId, storeId, discountId):
        if self.check_access():
            return True
        return self._real_subject.removeDiscount( userId, storeId, discountId)

    def createProductWeightRule(self, sid, pid, less_than, bigger_than):
        if self.check_access():
            return True
        return self._real_subject.createProductWeightRule( sid, pid, less_than, bigger_than)

    def createStoreWeightRule(self, uid, pid, less_than, bigger_than):
        if self.check_access():
            return True
        return self._real_subject.createStoreWeightRule(uid, pid, less_than, bigger_than)

    def createProductWeightRule(self, userId, pid, less_than, bigger_than):
        if self.check_access():
            return True
        return self._real_subject.createProductWeightRule(userId, pid, less_than, bigger_than)

    def createStoreTotalPriceLessThanRule(self, userId, pid, less_than, bigger_than):
        if self.check_access():
            return True
        return self._real_subject.createStoreTotalPriceLessThanRule(userId, pid, less_than, bigger_than)

    def createStoreQuantityLessThanRule(self, userId, pid, less_than, bigger_than):
        if self.check_access():
            return True
        return self._real_subject.createStoreQuantityLessThanRule(userId, pid, less_than, bigger_than)

    def createCategoryRule(self, userId, pid, less_than, bigger_than):
        if self.check_access():
            return True
        return self._real_subject.createCategoryRule(userId, pid, less_than, bigger_than)

    def createProductRule(self, userId, pid, less_than, bigger_than):
        if self.check_access():
            return True
        return self._real_subject.createProductRule(userId, pid, less_than, bigger_than)


    # def define_purchase(self, store_id, purchase):
    #     if self._real_subject is None:
    #         if purchase is None or store_id < 0:
    #             return False
    #         return True
    #     return self._real_subject.define_purchase(id, purchase)
    #
    # def discount_store(self, id, discount):
    #     if self._real_subject is None:
    #         if discount < 0:
    #             return False
    #         return True
    #     return self._real_subject.discount_store(id, discount)
    #
    # def discount_prod(self, store_id, prod_id, discount):
    #     if self._real_subject is None:
    #         if discount < 0 or store_id < 0 or prod_id < 0:
    #             return False
    #         return True
    #     return self._real_subject.discount_prod(store_id, prod_id , discount)

    # def edit_purchase(self, store_id, new_purchase):
    #     if self._real_subject is None:
    #         if new_purchase is None:
    #             return False
    #         return True
    #     return self._real_subject.edit_purchase(store_id, new_purchase)
    #
    # def edit_discount(self, store_id, new_discount):
    #     if self._real_subject is None:
    #         if new_discount < 0:
    #             return False
    #         return True
    #     return self._real_subject.edit_discount(store_id, new_discount)
