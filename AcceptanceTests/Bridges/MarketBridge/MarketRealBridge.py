from interface import implements
import IMarketBridge


class MarketRealBridge(implements(IMarketBridge)):

    def request(self):
        print("RealSubject: Handling request.")
