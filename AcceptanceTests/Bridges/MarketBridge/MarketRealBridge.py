from interface import implements
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge


class MarketRealBridge(implements(IMarketBridge)):
    def __init__(self, market_service):
        self._market_service = market_service

    def request(self):
        print("RealSubject: Handling request.")

    def search_product(self, product_name, category, price_min, price_max, product_rating, store_rating):
        ret = self._market_service.getProductsByName(product_name)
        if ret is None:
            return self._market_service.getProductByCatagory(category)


