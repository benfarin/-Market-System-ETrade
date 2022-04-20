from Business.MarketManage import MarketManage
from interfaces import IMarket
class MarketService:
    def __init__(self):
        self.__market: IMarket = MarketManage()
    def asd(self):
        self.__market.printPurchaseHistoryInformation(12341243,"asfdas")
