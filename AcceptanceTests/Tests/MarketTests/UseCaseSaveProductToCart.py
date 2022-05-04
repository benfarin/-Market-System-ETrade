import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseSaveProductToCart(unittest.TestCase):
    def setUp(self):
        self.market_proxy = MarketProxyBridge(MarketRealBridge())
        self.user_proxy = UserProxyBridge(UserRealBridge())
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim")
        self.user_proxy.login_member("user1", "1234")
        self.store_id = self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000")
        self.product1 = self.market_proxy.add_product_to_store(self.store_id, self.user_id, "Product", 500,
                                                      "Category", ["Test1", "Test2"])
        self.market_proxy.add_quantity_to_store(self.store_id, self.user_id, self.product1.getProductId(), 100)

    def test_add_to_cart_positive1(self):
        self.assertEqual(self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1.getProductId(), 10), True)
        self.assertEqual(self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1.getProductId(), 30), True)

    def test_add_to_cart_negative1(self):
        self.assertRaises(Exception, self.user_proxy.add_product_to_cart(self.user_id, self.store_id, -50, 10))

    def test_add_to_cart_negative2(self):
        self.assertRaises(Exception, self.user_proxy.add_product_to_cart(self.user_id, -50, self.product1, 10))

    def test_add_to_cart_negative3(self):
        self.assertRaises(Exception, self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1, 2500))


if __name__ == '__main__':
    unittest.main()
