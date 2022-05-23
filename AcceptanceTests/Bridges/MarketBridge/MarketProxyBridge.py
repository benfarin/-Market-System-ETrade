import zope
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge
from AcceptanceTests.Bridges.MarketBridge import MarketRealBridge
from Backend.Business.Rules.ruleCreator import ruleCreator


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

    def addSimpleDiscount_Category(self, userId, storeId, precent, category):
        if self.check_access():
            return True
        return self._real_subject.addSimpleDiscount_Category(userId, storeId, precent, category)

    def addSimpleDiscount_Product(self, userId, storeId, precent, productId):
        if self.check_access():
            return True
        return self._real_subject.addSimpleDiscount_Product(userId, storeId, precent, productId)

    def addConditionDiscountAdd(self, userId, storeId, dId1, dId2):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountAdd(userId, storeId, dId1, dId2)

    def addConditionDiscountMax(self, userId, storeId, dId1, dId2):
        if self.check_access():
            return True
        return self._real_subject.addConditionDiscountMax(userId, storeId, dId1, dId2)

    def removeDiscount(self,  userId, storeId, discountId):
        if self.check_access():
            return True
        return self._real_subject.removeDiscount( userId, storeId, discountId)


