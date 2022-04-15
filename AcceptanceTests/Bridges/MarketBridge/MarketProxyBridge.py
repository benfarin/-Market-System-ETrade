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
        return self._real_subject is not None

    def add_product(self, prod_id, store_id, name, price, category):
        if self._real_subject is None:
            if price < 0 or store_id < 0 or prod_id < 0:
                return False
            return True
        else:
            return self._real_subject.add_product(prod_id, store_id, name, price, category)

    def add_store(self, store_id, name):
        if self._real_subject is None:
            if name is None or store_id < 0:
                return False
            return True
        else:
            return self._real_subject.add_store(store_id, name)

    def remove_product(self, store_id, prod_id):
        if self._real_subject is None:
            if store_id < 0 or prod_id < 0:
                return False
            return True
        return self._real_subject.remove_product(store_id, prod_id)

    def edit_product_price(self, store_id, prod_id , new_price):
        if self._real_subject is None:
            if new_price < 0 or store_id < 0 or prod_id < 0:
                return False
            return True
        return self._real_subject.edit_product_price(store_id, prod_id ,new_price)

    def edit_product_name(self, store_id, prod_id, new_name):
        if self._real_subject is None:
            if new_name is None or store_id < 0 or prod_id < 0:
                return False
            return True
        return self._real_subject.edit_product_name(store_id, prod_id, new_name)

    def edit_product_category(self, store_id, prod_id, new_category):
        if self._real_subject is None:
            if new_category is None or store_id < 0 or prod_id < 0:
                return False
            return True
        return self._real_subject.edit_product_category(store_id, prod_id, new_category)

    def define_purchase(self, store_id, purchase):
        if self._real_subject is None:
            if purchase is None or store_id < 0:
                return False
            return True
        return self._real_subject.define_purchase(id, purchase)

    def define_discount(self, id, discount):
        if self._real_subject is None:
            if discount < 0:
                return False
            return True
        return self._real_subject.define_purchase(id, discount)

    def discount_prod(self, store_id, prod_id, discount):
        if self._real_subject is None:
            if discount < 0 or store_id < 0 or prod_id < 0:
                return False
            return True
        return self._real_subject.define_purchase(store_id, prod_id , discount)

    def close_store(self, store_id):
        if self._real_subject is None:
            if store_id < 0:
                return False
            return True
        return self._real_subject.close_store(store_id)

