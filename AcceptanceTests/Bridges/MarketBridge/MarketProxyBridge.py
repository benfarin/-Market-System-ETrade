from interface import implements
import IMarketBridge
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
            return False
        else:
            return self._real_subject.add_product(id, name, price, category)
