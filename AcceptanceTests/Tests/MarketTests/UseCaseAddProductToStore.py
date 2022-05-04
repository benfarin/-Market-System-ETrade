import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseAddProduct(unittest.TestCase):
    # use-case 4.1.1

    def setUp(self):
        self.proxy_market = MarketProxyBridge(MarketRealBridge(MemberService()))
        self.proxy_user = UserProxyBridge(UserRealBridge(UserService(), MemberService()))

        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.user_id = self.proxy_user.register("testUser", "1234", "0540000000", 123,[] ,"Israel", "Beer Sheva", "Rager", 1, "testBank")
        self.proxy_user.login_member("testUser", "1234")
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000)


    def test_addProductPositive(self):
        # store_id, user_id, name, price, category, key_words
        try:
            self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, "testCategory", ["test"])
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)

    def test_addProductNegativePrice(self):
        # price is negative
        self.assertRaises(Exception, self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", -20, "testCategory", ["test"]))

    def test_addProductNoCategory(self):
        # no category
        self.assertRaises(Exception, self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, None, ["test"]))

    def test_addProductIllegalStoreId(self):
        # illegal store id
        self.assertRaises(Exception, self.proxy_market.add_product_to_store(-1, self.user_id, "testProduct", 10, "testCategory", ["test"]))

    def test_addProductIllegalUserId(self):
        # illegal user id
        self.assertRaises(Exception, self.proxy_market.add_product_to_store(self.store_id, -1, "testProduct", 10, "testCategory", ["test"]))


if __name__ == '__main__':
    unittest.main()
