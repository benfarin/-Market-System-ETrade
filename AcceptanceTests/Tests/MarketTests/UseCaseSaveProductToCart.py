import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MarketService import MarketService
from Service.UserService import UserService


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.market_proxy = MarketProxyBridge(MarketService())
        self.user_proxy = UserProxyBridge(UserRealBridge(UserService(), MarketService()))
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim", None)
        self.store_id = self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000")
        self.product1 = self.market_proxy.add_product_to_store(self.store_id, self.user_id, "Product", 500,
                                                      "Category", ["Test1", "Test2"])

    def test_add_to_cart_positive1(self):
        self.assertEqual(self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1, 10), True)
        self.assertEqual(self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1, 30), True)

    def test_add_to_cart_negative1(self):
        self.assertEqual(self.user_proxy.add_product_to_cart(self.user_id, self.store_id, -50, 10), False)

    def test_add_to_cart_negative2(self):
        self.assertEqual(self.user_proxy.add_product_to_cart(self.user_id, -50, self.product1, 10), False)

    def test_add_to_cart_negative3(self):
        self.assertEqual(self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1, 2500), False)


if __name__ == '__main__':
    unittest.main()
