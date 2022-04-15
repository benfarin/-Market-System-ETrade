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

    def add_product(self, id, name, price, category):
        if self._real_subject is None:
            if price >= 0:
                return True
            return False
        else:
            return self._real_subject.add_product(id, name, price, category)

    def add_store(self, id, name):
        if self._real_subject is None:
            if name is not None:
                return True
            return False
        else:
            return self._real_subject.add_store(id, name)

    def remove_product(self, id):
        if self._real_subject is None:
            return True
        return self._real_subject.remove_product(id)

    def edit_product_price(self, id, new_price):
        if self._real_subject is None:
            if new_price <= 0:
                return False
            return True
        return self._real_subject.edit_product_price(id, new_price)

    def edit_product_name(self, id, new_name):
        if self._real_subject is None:
            if new_name is None:
                return False
            return True
        return self._real_subject.edit_product_name(id, new_name)

    def edit_product_category(self, id, new_category):
        if self._real_subject is None:
            if new_category == None:
                return False
            return True
        return self._real_subject.edit_product_category(id, new_category)

    def define_purchase(self, id, purchase):
        if self._real_subject is None:
            return True
        return self._real_subject.define_purchase(id, purchase)
