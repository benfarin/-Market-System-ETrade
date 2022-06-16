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

    def setUp(self):

        # assign system manager
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "Manager", "1234")
        # Create 3 users
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Rotem", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Bar", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Kfir", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 0)

        # 3 users log-in
        self.user_id1 = self.proxy_user.login_member(self.__guestId1, "Rotem", "1234").getData().getUserID()
        self.user_id2 = self.proxy_user.login_member(self.__guestId2, "Bar", "1234").getData().getUserID()
        self.user_id3 = self.proxy_user.login_member(self.__guestId3, "Kfir", "1234").getData().getUserID()

        # Create store
        self.store_id1 = self.proxy_user.open_store("testStore1", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()

    def tearDown(self):
        # remove store
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id1)
        # remove users
        self.proxy_user.removeMember("Manager", "Rotem")
        self.proxy_user.removeMember("Manager", "Bar")
        self.proxy_user.removeMember("Manager", "Kfir")
        # remove manager
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_addProductPositive(self):
        # add 2 products to store1
        p1_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
                                                       "testCategory", 15, ["test"]).getData().getProductId()
        p2_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct2", 100,
                                                       "testCategory", 10, ["test"]).getData().getProductId()
        # get all products from store1
        storeProductsIds = [pId for pId in
                            self.proxy_market.get_store_by_ID(self.store_id1).getData().getProducts().keys()]
        # check both product id's are in store
        self.assertEqual(storeProductsIds, [p1_id, p2_id])
        # check both product id's are different
        self.assertNotEqual(p1_id, p2_id)

    def test_addProduct_negative(self):
        # price is negative
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct", -20,
                                                               "testCategory", 10, ["test"]).isError())
        # no store owner to add products
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, -1, "prod", 20, "catergory", 2, ["key"]).isError)

    def test_add_product_permission(self):
        # user2 has no permission to add products to store
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, self.user_id2, "testProduct1", 10,
                                                       "testCategory", 15, ["test"]).isError())
        self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "Bar")
        # now user2 has permission to add products
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, self.user_id2, "testProduct2", 10,
                                                               "testCategory", 15, ["test"]).getData())
        # manager doesn't have permission to add products to store
        self.proxy_market.appoint_store_manager(self.store_id1, self.user_id1, "Kfir")
        self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, self.user_id3, "testProduct", 10,
                                                               "testCategory", 15, ["test"]).isError())

    # def test_product_with_same_name(self):
    #     self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
    #                                                    "testCategory", 15, ["test"]).getData())
    #     self.assertTrue(self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
    #                                                    "testCategory", 15, ["test"]).isError())


if __name__ == '__main__':
    unittest.main()
