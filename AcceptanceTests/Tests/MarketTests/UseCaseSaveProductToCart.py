import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.market_proxy = MarketProxyBridge(None)
        self.user_proxy = UserProxyBridge(None)
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim", None)
        self.store_id = self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000")
        self.product1 = self.market_proxy.add_product(self.store_id, self.user_id, "Product", 500,
                                                      "Category", ["Test1", "Test2"])

    def test_add_to_cart_positive1(self):
        self.assertEqual(self.user_proxy., True)

    def test_add_to_cart_negative1(self):
        self.assertEqual(self.user_proxy.add_product("TestUser", 0, 1, 10), False)

    def test_add_to_cart_negative2(self):
        self.assertEqual(self.user_proxy.add_product("TestUser", 1, 0, 10), False)

    def test_add_to_cart_negative3(self):
        self.assertEqual(self.user_proxy.add_product("TestUser", -1, 0, 10), False)

    def tearDown(self):
        self.market_proxy.close_store(0)
        self.market_proxy.remove_product(0, 0)
        self.user_proxy.delete_user("TestUser", "TestPassword")


if __name__ == '__main__':
    unittest.main()
