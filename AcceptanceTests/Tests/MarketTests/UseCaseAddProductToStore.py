import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseAddProduct(unittest.TestCase):
    # use-case 4.1.1
    @classmethod
    def setUpClass(cls):
        cls.proxy_market = MarketProxyBridge(MarketRealBridge())
        cls.proxy_user = UserProxyBridge(UserRealBridge())

        cls.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        cls.proxy_user.register("testUser", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        cls.user_id = cls.proxy_user.login_member("testUser", "1234").getData().getUserID()
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        cls.store_id = cls.proxy_user.open_store("testStore", cls.user_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()


    def test_addProductPositive(self):
        # store_id, user_id, name, price, category, key_words
        try:
            self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, "testCategory", ["test"])
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)

    def test_addProductNegativePrice(self):
        # price is negative
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", -20, "testCategory", ["test"]).isError())

    def test_addProductNoCategory(self):
        # no category
        self.assertTrue(Exception, lambda: self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, None, ["test"]).isError())

    def test_addProductIllegalStoreId(self):
        # illegal store id
        self.assertTrue(Exception, lambda: self.proxy_market.add_product_to_store(-1, self.user_id, "testProduct", 10, "testCategory", ["test"]).isError())

    def test_addProductIllegalUserId(self):
        # illegal user id
        self.assertTrue(Exception, lambda: self.proxy_market.add_product_to_store(self.store_id, -1, "testProduct", 10, "testCategory", ["test"]).isError())


if __name__ == '__main__':
    unittest.main()
