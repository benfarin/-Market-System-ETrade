from interface import implements
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge
from AcceptanceTests.Bridges.MarketBridge import MarketRealBridge


class MarketProxyBridge(implements(IMarketBridge)):
    def __init__(self, real_subject: MarketRealBridge):
        self._real_subject = real_subject

    def request(self) -> bool:
        if self.check_access():
            self._real_subject.request()
        else:
            return True

    def check_access(self) -> bool:
        return self._real_subject is None

    def add_product_to_store(self, store_id, user_id, name, price, category, key_words):
        if self.check_access():
            return True
        else:
            return self._real_subject.add_product_to_store(store_id, user_id, name, price, category, key_words)

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

    def close_store(self, store_id):
        if self.check_access():
            if store_id < 0:
                return False
            return True
        return self._real_subject.close_store(store_id)

    # def edit_product_name(self, store_id, prod_id, new_name):
    #     if self._real_subject is None:
    #         if new_name is None or store_id < 0 or prod_id < 0:
    #             return False
    #         return True
    #     return self._real_subject.edit_product_name(store_id, prod_id, new_name)
    #
    # def edit_product_category(self, store_id, prod_id, new_category):
    #     if self._real_subject is None:
    #         if new_category is None or store_id < 0 or prod_id < 0:
    #             return False
    #         return True
    #     return self._real_subject.edit_product_category(store_id, prod_id, new_category)

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

    # def get_store_info(self, store_id):
    #     if self._real_subject is None:
    #         if store_id < 0:
    #             return False
    #         return True
    #     return self._real_subject.get_store_info(store_id)

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

    # def get_cart_info(self, username):
    #     if self.check_access():
    #         return True
    #     return self._real_subject.get_cart_info(username)