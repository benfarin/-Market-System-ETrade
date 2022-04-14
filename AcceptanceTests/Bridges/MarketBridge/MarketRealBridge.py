from interface import implements
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge


class MarketRealBridge(implements(IMarketBridge)):
    def __init__(self, market_service):
        self._market_service = market_service


    def request(self):
        print("RealSubject: Handling request.")
