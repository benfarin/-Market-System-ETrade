import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService
from Service.Response import Response
from Service.DTO.StoreDTO import StoreDTO


class UseCaseGetEditUserCart(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.market_proxy = MarketProxyBridge(MarketRealBridge())
        self.user_proxy = UserProxyBridge(UserRealBridge())
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim")
        self.user_id = self.user_proxy.login_member("user1", "1234").getData().getMemberId()
        self.store_id = self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").getData().getStoreId()
        self.product1 = self.market_proxy.add_product_to_store(self.store_id, self.user_id, "Product", 500,
                                                               "Category", ["Test1", "Test2"]).getData()
        self.market_proxy.add_quantity_to_store(self.store_id, self.user_id, self.product1.getProductId(), 100)

    def test_get_cart_info_positive1(self):
        try:
            self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1.getProductId(), 10)
            print(self.market_proxy.get_cart_info(self.user_id).getData())
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_get_cart_info_negative1(self):
        self.assertRaises(Exception, self.market_proxy.get_cart_info(-999))

    def test_edit_cart_info_positive1(self):
        old_info = self.market_proxy.get_cart_info(self.user_id)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_id, self.product1.getProductId(), 50)
        new_info = self.market_proxy.get_cart_info(self.user_id)
        self.assertNotEqual(old_info, new_info)

    # def test_edit_cart_info_negative1(self):  # NEED TO EDIT THIS
    #     old_info = self.user_proxy.get_cart_info("User1")
    #     new_info = self.user_proxy.add_product_to_cart(1, 0, 5)
    #     self.assertEqual(old_info, new_info)


if __name__ == '__main__':
    unittest.main()
