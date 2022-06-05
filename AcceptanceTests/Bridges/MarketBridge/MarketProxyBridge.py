import zope
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge
from AcceptanceTests.Bridges.MarketBridge import MarketRealBridge


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
            return True
        return self._real_subject.remove_product_from_store(store_id, user_id, prod_id)

    def edit_product_price(self,user_id,  store_id, prod_id, new_price):
        if self.check_access():
            return True
        return self._real_subject.edit_product_price(user_id, store_id, prod_id, new_price)

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

    def removeStoreOwner(self, storeId, assignerId, assigneeName):
        if self.check_access():
            return True
        return self._real_subject. removeStoreOwner(storeId, assignerId, assigneeName)

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

    def removeStoreForGood(self, userId, storeId):
        if self.check_access():
            return True
        return self._real_subject.removeStoreForGood(userId, storeId)


    def get_store_info(self, store_id, user_id):
        if self.check_access():
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

    def addSimpleDiscount_Category(self, userId, storeId, category,precent):
        if self.check_access():
            return True
        return self._real_subject.addSimpleDiscount_Category(userId, storeId, category,precent)

    def addSimpleDiscount_Product(self, userId, storeId, productId,precent):
        if self.check_access():
            return True
        return self._real_subject.addSimpleDiscount_Product(userId, storeId,productId ,precent)

    def addConditionDiscountAdd(self, userId, storeId, dId1, dId2):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountAdd(userId, storeId, dId1, dId2)

    def addConditionDiscountMax(self, userId, storeId, dId1, dId2):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountMax(userId, storeId, dId1, dId2)

    def addConditionDiscountXor(self, userId, storeId, dId1, dId2, decide):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountXor(userId, storeId, dId1, dId2, decide)

    def removeDiscount(self,  userId, storeId, discountId):
        if self.check_access():
            return True
        return self._real_subject.removeDiscount(userId, storeId, discountId)

    def addStoreTotalAmountDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addStoreTotalAmountDiscountRule(userId, storeId, discountId, atLeast, atMost)

    def addStoreQuantityDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addStoreQuantityDiscountRule(userId, storeId, discountId, atLeast, atMost)

    def addCategoryQuantityDiscountRule(self, userId, storeId, discountId, category, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addCategoryQuantityDiscountRule(userId, storeId, discountId, category, atLeast, atMost)

    def addProductQuantityDiscountRule(self, userId, storeId, discountId, productId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addProductQuantityDiscountRule(userId, storeId, discountId, productId, atLeast, atMost)

    def addStoreWeightDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addStoreWeightDiscountRule(userId, storeId, discountId, atLeast, atMost)

    def addCategoryWeightDiscountRule(self, userId, storeId, discountId, category, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addCategoryWeightDiscountRule(userId, storeId, discountId, category, atLeast, atMost)

    def addProductWeightDiscountRule(self, userId, storeId, discountId, productId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addProductWeightDiscountRule(userId, storeId, discountId, productId, atLeast, atMost)

    def addCompositeRuleDiscountAnd(self, userId, storeId, dId, rId1, rId2):
        if self.check_access():
            return True
        return self._real_subject.addCompositeRuleDiscountAnd(userId, storeId, dId, rId1, rId2)

    def addCompositeRuleDiscountOr(self, userId, storeId, dId, rId1, rId2):
        if self.check_access():
            return True
        return self._real_subject.addCompositeRuleDiscountOr(userId, storeId, dId, rId1, rId2)

    def removeRuleDiscount(self, userId, storeId, dId, rId):
        if self.check_access():
            return True
        return self._real_subject.removeRuleDiscount(userId, storeId, dId, rId)

    #Purchase rules
    def addStoreTotalAmountPurchaseRule(self, userId, storeId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addStoreTotalAmountPurchaseRule(userId, storeId, atLeast, atMost)

    def addStoreQuantityPurchaseRule(self, userId, storeId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addStoreQuantityPurchaseRule(userId, storeId, atLeast, atMost)

    def addCategoryQuantityPurchaseRule(self, userId, storeId, category, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addCategoryQuantityPurchaseRule(userId, storeId, category, atLeast, atMost)

    def addProductQuantityPurchaseRule(self, userId, storeId, productId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addProductQuantityPurchaseRule(userId, storeId, productId, atLeast, atMost)

    def addStoreWeightPurchaseRule(self, userId, storeId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addStoreWeightPurchaseRule(userId, storeId, atLeast, atMost)

    def addCategoryWeightPurchaseRule(self, userId, storeId, category, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addCategoryWeightPurchaseRule(userId, storeId, category, atLeast, atMost)

    def addProductWeightPurchaseRule(self, userId, storeId, productId, atLeast, atMost):
        if self.check_access():
            return True
        return self._real_subject.addProductWeightPurchaseRule(userId, storeId, productId, atLeast, atMost)

    def addCompositeRulePurchaseAnd(self, userId, storeId, rId1, rId2):
        if self.check_access():
            return True
        return self._real_subject.addCompositeRulePurchaseAnd(userId, storeId, rId1, rId2)

    def addCompositeRulePurchaseOr(self, userId, storeId, rId1, rId2):
        if self.check_access():
            return True
        return self._real_subject.addCompositeRulePurchaseOr(userId, storeId, rId1, rId2)

    def removeRulePurchase(self, userId, storeId, rId):
        if self.check_access():
            return True
        return self._real_subject.removeRulePurchase(userId, storeId, rId)

    def appoint_owner_perm(self, store_id, assigner_id, assignee_name):
        if self.check_access():
            return True
        return self._real_subject.appoint_owner_perm(store_id, assigner_id, assignee_name)

    def set_roles_info_perm(self, store_id, assigner_id, assignee_name):
        if self.check_access():
            return True
        return self._real_subject.set_roles_info_perm(store_id, assigner_id, assignee_name)

    def set_purchase_history_info_perm(self, store_id, assigner_id, assignee_name):
        if self.check_access():
            return True
        return self._real_subject.set_purchase_history_info_perm(store_id, assigner_id, assignee_name)

    def set_discount_perm(self, store_id, assigner_id, assignee_name):
        if self.check_access():
            return True
        return self._real_subject.set_discount_perm(store_id, assigner_id, assignee_name)

    def remove_member(self, admin_name, member_name):
        if self.check_access():
            return True
        return self._real_subject.remove_member(admin_name, member_name)

    def get_all_store_trans(self, admin_name):
        if self.check_access():
            return True
        return self._real_subject.get_all_store_trans(admin_name)

    def get_all_user_trans(self, admin_name):
        if self.check_access():
            return True
        return self._real_subject.get_all_user_trans(admin_name)

    def get_user_tran(self, admin_name, tran_id):
        if self.check_access():
            return True
        return self._real_subject.get_user_tran(admin_name, tran_id)

    def get_store_tran_by_store_id(self, admin_name, store_id):
        if self.check_access():
            return True
        return self._real_subject.get_store_tran_by_store_id(admin_name, store_id)

    def get_all_rules(self, user_id, store_id):
        if self.check_access():
            return True
        return self._real_subject.get_all_rules(user_id, store_id)