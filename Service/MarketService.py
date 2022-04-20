from Business.MarketManage import MarketManage
from interfaces import IMarket
class MarketService:
    def __init__(self):
        self__market: IMarket = MarketManage()
