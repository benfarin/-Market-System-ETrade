import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService


class UseCaseAddProduct(unittest.TestCase):
    # use-case 4.1.1

    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    # @classmethod
    def setUp(self):

        # assign system manager
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(admin_id, "Manager", "1234")
        # Create 3 users
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser1", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 0)

        # 3 users log-in
        self.user_id1 = self.proxy_user.login_member(self.__guestId1, "testUser1", "1234").getData().getUserID()
        self.user_id2 = self.proxy_user.login_member(self.__guestId2, "testUser2", "1234").getData().getUserID()
        self.user_id3 = self.proxy_user.login_member(self.__guestId3, "testUser3", "1234").getData().getUserID()

        # Create 3 stores
        self.store_id1 = self.proxy_user.open_store("testStore1", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()
        self.store_id2 = self.proxy_user.open_store("testStore2", self.user_id2, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()
        self.store_id3 = self.proxy_user.open_store("testStore3", self.user_id3, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()

    def tearDown(self) -> None:
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id1)
        self.proxy_market.removeStoreForGood(self.user_id2, self.store_id2)
        self.proxy_market.removeStoreForGood(self.user_id3, self.store_id3)
        self.proxy_user.removeMember("Manager", "testUser1")
        self.proxy_user.removeMember("Manager", "testUser2")
        self.proxy_user.removeMember("Manager", "testUser3")
        self.proxy_user.removeMember("Manager")


    def test_addProductPositive(self):
        p1_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
                                                       "testCategory", 15, ["test"]).getData().getProductId()
        p2_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct2", 100,
                                                       "testCategory", 10, ["test"]).getData().getProductId()
        storeProductsIds = [pId for pId in
                            self.proxy_market.get_store_by_ID(self.store_id1).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [p1_id, p2_id])
        self.assertNotEqual(p1_id, p2_id)

    def test_addProductNegativePrice(self):
        # price is negative
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct", -20,
                                                               "testCategory", 10, ["test"]).isError())
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id2, self.user_id2, "testProduct", -1,
                                                               "testCategory", 10, ["test"]).isError())

    def test_addProductNoCategory(self):
        # no category
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1",
                                                               10, "Category", 10, ["test"]).isError())
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id2, self.user_id2, "testProduct2",
                                                               10, "Category1", 10, ["test"]).isError())

    def test_addProductIllegalStoreId(self):
        # illegal store id
        self.assertTrue(self.proxy_market.add_product_to_store(-1, self.user_id1, "testProduct", 10,
                                                               "testCategory", 10, ["test"]).isError())
        self.assertTrue(self.proxy_market.add_product_to_store(11, self.user_id1, "testProduct", 10,
                                                               "testCategory", 10, ["test"]).isError())

    def test_addProductIllegalUserId(self):
        # illegal user id
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, -1, "testProduct", 10,
                                                               "testCategory", 10, ["test"]).isError())
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, 8, "testProduct", 10,
                                                               "testCategory", 10, ["test"]).isError())


if __name__ == '__main__':
    unittest.main()
