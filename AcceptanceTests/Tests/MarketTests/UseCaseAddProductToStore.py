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
        cls.__guestId1 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser1", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1,
                                "testBank")
        cls.__guestId2 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser2", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1,
                                "testBank")
        cls.__guestId3 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser3", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1,
                                "testBank")

        cls.user_id1 = cls.proxy_user.login_member(cls.__guestId1, "testUser1", "1234").getData().getUserID()
        cls.user_id2 = cls.proxy_user.login_member(cls.__guestId2, "testUser2", "1234").getData().getUserID()
        cls.user_id3 = cls.proxy_user.login_member(cls.__guestId3, "testUser3", "1234").getData().getUserID()

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        cls.store_id1 = cls.proxy_user.open_store("testStore1", cls.user_id1, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()
        cls.store_id2 = cls.proxy_user.open_store("testStore2", cls.user_id2, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()
        cls.store_id3 = cls.proxy_user.open_store("testStore3", cls.user_id3, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

    def test_addProductPositive(self):
        # store_id, user_id, name, price, category, key_words
        product = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10, "testCategory", 15,
                                               ["test"])
        self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct2", 100, "testCategory", 10,
                                               ["test"])
        self.proxy_market.add_product_to_store(self.store_id3, self.user_id1, "testProduct3", 100, "testCategory", 12,
                                               ["test"])
        self.assertEqual(0, product.getData().getProductId())

    def test_addProductNegativePrice(self):
        # price is negative
        self.assertTrue(
            self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct", -20, "testCategory", 10,
                                                   ["test"]).isError())
        self.assertTrue(
            self.proxy_market.add_product_to_store(self.store_id2, self.user_id2, "testProduct", -1, "testCategory", 10,
                                                   ["test"]).isError())

    def test_addProductNoCategory(self):
        # no category
        self.assertTrue(Exception,
                        lambda: self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
                                                                       10, None, ["test"]).isError())
        self.assertTrue(Exception,
                        lambda: self.proxy_market.add_product_to_store(self.store_id2, self.user_id2, "testProduct2", 10,
                                                                       10, None, ["test"]).isError())

    def test_addProductIllegalStoreId(self):
        # illegal store id
        self.assertTrue(Exception, lambda: self.proxy_market.add_product_to_store(-1, self.user_id1, "testProduct", 10,
                                                                                  "testCategory", 10, ["test"]).isError())
        self.assertTrue(Exception,
                        lambda: self.proxy_market.add_product_to_store(-1000, self.user_id1, "testProduct", 10,
                                                                       "testCategory", 10, ["test"]).isError())

    def test_addProductIllegalUserId(self):
        # illegal user id
        self.assertTrue(Exception, lambda: self.proxy_market.add_product_to_store(self.store_id1, -1, "testProduct", 10,
                                                                                  "testCategory", 10, ["test"]).isError())
        self.assertTrue(Exception,
                        lambda: self.proxy_market.add_product_to_store(self.store_id1, -1512, "testProduct", 10,
                                                                       "testCategory", 10, ["test"]).isError())


if __name__ == '__main__':
    unittest.main()
