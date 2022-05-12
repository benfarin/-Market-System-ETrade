import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCasePurchaseProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.market_proxy = MarketProxyBridge(MarketRealBridge())
        cls.user_proxy = UserProxyBridge(UserRealBridge())
        cls.user_proxy.appoint_system_manager("user1", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        cls.__guestId = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register(cls.__guestId, "user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim")
        cls.user_id = cls.user_proxy.login_member("user1", "1234").getData().getUserID()
        cls.store_id = cls.user_proxy.open_store("store", cls.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").getData().getStoreId()
        cls.product1 = cls.market_proxy.add_product_to_store(cls.store_id, cls.user_id, "Product", 500,
                                                               "Category", ["Test1", "Test2"]).getData()
        cls.market_proxy.add_quantity_to_store(cls.store_id, cls.user_id, cls.product1.getProductId(), 100)

    def test_purchase_positive1(self):
        self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1.getProductId(), 20)
        try:
            self.user_proxy.purchase_product(self.user_id, 500, 20)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_guest_then_member_purchase(self):
        guest2_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.add_product_to_cart(guest2_id, self.store_id, self.product1.getProductId(), 20)
        self.user_proxy.register(guest2_id, "user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, "HaPoalim")
        self.user2_id = self.user_proxy.login_member("user2", "1234").getData().getUserID()
        try:
            userTransaction1 = self.user_proxy.purchase_product(self.user2_id, 500, 20).getData()
            print(userTransaction)
        except:
            self.assertTrue(False)

    def test_purchase_negative1(self):
        self.assertRaises(Exception, self.user_proxy.purchase_product("user1", 1, 30))

    def test_purchase_negative2(self):
        self.assertRaises(Exception, self.user_proxy.purchase_product("user1", 500, 30))

    def test_purchase_negative3(self):
        self.assertRaises(Exception, self.user_proxy.purchase_product("User1", 1, 20))


if __name__ == '__main__':
    unittest.main()
