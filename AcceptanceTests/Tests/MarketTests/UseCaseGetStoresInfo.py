import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MarketService import MarketService
from Service.UserService import UserService


class UseCaseGetStoresInfo(unittest.TestCase):
    def setUp(self):
        self.user_proxy = UserProxyBridge(UserRealBridge(UserService(), MarketService()))
        self.market_proxy = MarketProxyBridge(MarketService())

    # def test_get_stores_info_positive(self):
    #     self.market_proxy.add_store(0, "TestStore")
    #     self.assertEqual(self.market_proxy.get_store_info(0), True)
    #
    # def test_get_stores_info_negative(self):
    #     self.assertEqual(self.market_proxy.get_store_info(-50), False)


if __name__ == '__main__':
    unittest.main()
