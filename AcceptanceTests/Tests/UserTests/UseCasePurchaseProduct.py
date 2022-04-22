import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.user_proxy = UserProxyBridge(None)
        self.market_proxy = MarketProxyBridge(None)
        self.user_proxy.register("User1", "Pass", "Pass", "Mail@Mail.com")
        self.user_proxy.login("User1", "Pass")
        self.market_proxy.add_store(0, "Store")
        self.market_proxy.add_product(0, 0, "TestProduct", 10, "Category")
        self.market_proxy.add_product(1, 0, "TestProduct2", 20, "Category")
        self.user_proxy.add_product("User1", 0, 0, 10)

    def test_purchase_positive1(self):
        self.assertEqual(self.user_proxy.purchase_product("User1", 0, 5), True)

    def test_purchase_negative1(self):
        self.assertEqual(self.user_proxy.purchase_product("User1", 1, 30), False)


if __name__ == '__main__':
    unittest.main()
