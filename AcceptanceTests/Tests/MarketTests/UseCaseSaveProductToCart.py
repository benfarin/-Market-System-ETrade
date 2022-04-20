import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.market_proxy = MarketProxyBridge(None)
        self.user_proxy = UserProxyBridge(None)
        self.market_proxy.add_store(0, "TestStore")
        self.market_proxy.add_product(0, 0, "Product1", 10, "Category1")
        self.user_proxy.register("TestUser", "TestPassword", "TestPassword", "TestEmail")

    def test_add_to_cart_positive1(self):
        self.assertEqual(self.user_proxy.add_product(0, 0, 10), True)

    def test_add_to_cart_negative1(self):
        self.assertEqual(self.user_proxy.add_product(0, 1, 10), False)

    def test_add_to_cart_negative2(self):
        self.assertEqual(self.user_proxy.add_product(1, 0, 10), False)

    def test_add_to_cart_negative3(self):
        self.assertEqual(self.user_proxy.add_product(-1, 0, 10), False)

    def tearDown(self):
        self.market_proxy.close_store(0)
        self.market_proxy.remove_product(0, 0)
        self.user_proxy.delete_user("TestUser", "TestPassword")


if __name__ == '__main__':
    unittest.main()
