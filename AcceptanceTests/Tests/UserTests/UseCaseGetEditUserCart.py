import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class UseCaseGetEditUserCart(unittest.TestCase):
    def setUp(self):
        self.user_proxy = UserProxyBridge(None)
        self.market_proxy = MarketProxyBridge(None)
        self.user_proxy.register("User1", "Pass", "Pass", "Mail@Mail.com")
        self.user_proxy.login("User1", "Pass")
        self.market_proxy.add_store(0, "Store")
        self.market_proxy.add_product_to_store(0, 0, "TestProduct", 10, "Category")
        self.market_proxy.add_product_to_store(1, 0, "TestProduct2", 20, "Category")
        self.user_proxy.add_product_to_cart(0, 0, 10)

    def test_get_cart_info_positive1(self):
        self.assertEqual(self.market_proxy.get_cart_info("User1"), True)

    def test_get_cart_info_negative1(self):
        self.assertEqual(self.market_proxy.get_cart_info("User2"), False)

    def test_edit_cart_info_positive1(self):
        old_info = self.user_proxy.get_cart_info("User1")
        new_info = self.user_proxy.add_product_to_cart(1, 0, 5)
        self.assertEqual(old_info, new_info)

    def test_edit_cart_info_negative1(self):  # NEED TO EDIT THIS
        old_info = self.user_proxy.get_cart_info("User1")
        new_info = self.user_proxy.add_product_to_cart(1, 0, 5)
        self.assertEqual(old_info, new_info)


if __name__ == '__main__':
    unittest.main()
