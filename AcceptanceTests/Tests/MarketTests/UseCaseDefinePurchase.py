import unittest
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MarketService import MarketService
from Service.UserService import UserService


class UseCaseDefinePurchase(unittest.TestCase):
    def setUp(self):
        self.proxyMarket = MarketProxyBridge(MarketService())
        self.proxyUser = UserProxyBridge(UserRealBridge(UserService(), MarketService()))

    # def test_definePurchasePositive(self):
    #     self.assertEqual(self.proxyMarket.define_purchase(0, "testPurchase"), True)
    #
    # def test_definePurchaseNegative(self):
    #     # store doesn't exist
    #     self.assertEqual(self.proxyMarket.define_purchase(-1, "testPurchase"), False)
    #
    # def test_definePurchaseNegative2(self):
    #     # purchase is none
    #     self.assertEqual(self.proxyMarket.define_purchase(0, None), False)


if __name__ == '__main__':
    unittest.main()
