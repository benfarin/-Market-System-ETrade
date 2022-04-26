import unittest
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseDefineDiscount(unittest.TestCase):
    def setUp(self):
        self.proxyMarket = MarketProxyBridge(None)
        self.proxyUser = UserProxyBridge(None)

    # def test_defineDiscountPositive(self):
    #     self.assertEqual(self.proxyMarket.discount_store(0, 20), True)
    #
    # def test_defineDiscountNegative(self):
    #     # store doesn't exist
    #     self.assertEqual(self.proxyMarket.define_purchase(-1, 20), False)
    #
    # def test_defineDiscountNegative2(self):
    #     # discount is negative
    #     self.assertEqual(self.proxyMarket.define_purchase(0, -10), False)


if __name__ == '__main__':
    unittest.main()
