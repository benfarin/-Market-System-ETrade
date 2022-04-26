import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class UseCaseGetEditUserCart(unittest.TestCase):
    def setUp(self):
        self.market_proxy = MarketProxyBridge(None)
        self.user_proxy = UserProxyBridge(None)
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim", None)
        self.store_id = self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000")
        self.product1 = self.market_proxy.add_product_to_store(self.store_id, self.user_id, "Product", 500,
                                                               "Category", ["Test1", "Test2"])

    def test_get_cart_info_positive1(self):
        self.assertEqual(self.market_proxy.get_cart_info(self.user_id), True)

    def test_get_cart_info_negative1(self):
        self.assertEqual(self.market_proxy.get_cart_info(-999), False)

    def test_edit_cart_info_positive1(self):
        old_info = self.user_proxy.get_cart_info("User1")
        self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1, 50)
        new_info = self.user_proxy.get_cart_info("User1")
        self.assertNotEqual(old_info, new_info)

    # def test_edit_cart_info_negative1(self):  # NEED TO EDIT THIS
    #     old_info = self.user_proxy.get_cart_info("User1")
    #     new_info = self.user_proxy.add_product_to_cart(1, 0, 5)
    #     self.assertEqual(old_info, new_info)


if __name__ == '__main__':
    unittest.main()
