import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UsePurchasesHistory(unittest.TestCase):
    def setUp(self):
        self.proxy_market = MarketProxyBridge(MarketRealBridge(MemberService()))
        self.proxy_user = UserProxyBridge(UserRealBridge(UserService(), MemberService()))
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva", "Ben Gurion", 1, 1)
        self.owner_id = self.proxy_user.register("testUser", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        self.proxy_user.login_member("testUser", "1234")
        self.store_id = self.proxy_user.open_store("testStore", self.owner_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000)
        self.prod1 = self.proxy_market.add_product_to_store(self.store_id, self.owner_id, "testProduct1", 10, "testCategory", ["testKeyWord"])
        self.proxy_market.add_quantity_to_store(self.store_id, self.owner_id, self.prod1.getProductId(), 100)
        self.prod2 = self.proxy_market.add_product_to_store(self.store_id, self.owner_id, "testProduct2", 50, "testCategory", ["testKeyWord"])
        self.proxy_market.add_quantity_to_store(self.store_id, self.owner_id, self.prod2.getProductId(), 100)
        self.user_id = self.proxy_user.register("testUser2", "1234", "0540030000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        self.proxy_user.login_member("testUser2", "1234")
        self.proxy_user.add_product_to_cart(self.user_id, self.store_id, self.prod1.getProductId(), 12)
        self.proxy_user.add_product_to_cart(self.user_id, self.store_id, self.prod2.getProductId(), 3)

    def test_get_purchases_history(self):
        # check buying
        try:
            print(self.proxy_market.get_cart(self.user_id))
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    # def test_get_purchases_history_info(self):
    #     self.proxy_market.get_cart(self.user_id)
    #     self.proxy_user.add_product_to_cart(self.user_id, self.store_id, self.prod2.getProductId(), 1)
    #     self.proxy_market.get_cart(self.user_id)
    #     print(self.proxy_market.print_purchase_history(self.store_id, self.user_id))


if __name__ == '__main__':
    unittest.main()
