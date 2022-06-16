import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseRemoveProduct(unittest.TestCase):

    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign system manager
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "Manager", "1234")

        # create user
        self.__guestId = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Bar", "1243", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.user_id = self.proxy_user.login_member(self.__guestId, "Bar", "1243").getData().getUserID()
        # create store
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, 1, "Israel", "Beer Sheva",
                                                   "Rager", 1, 00000).getData().getStoreId()
        # add product to store
        self.prod = self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10,
                                                           "testCategory", 10, ["testKeyWord"]).getData()
        # add product's quantity to store
        self.proxy_market.add_quantity_to_store(self.store_id, self.user_id, self.prod.getProductId(), 100)

    def tearDown(self):
        # remove store
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)
        # remove users
        self.proxy_user.removeMember("Manager", "Ori")
        self.proxy_user.removeMember("Manager", "Bar")
        # remove system manager
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_removeProductPositive(self):
        # check the product in the store
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [self.prod.getProductId()])
        # remove product from store
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId()).getData())
        # check no products in store
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [])

    def test_removeProductByManagerWithPermission(self):
        # create a user Ori
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Ori", "1243", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 0)
        user_id_2 = self.proxy_user.login_member(guestId2, "Ori", "1243").getData().getUserID()
        # appoint Ori to be a store's manager
        self.proxy_market.appoint_store_manager(self.store_id, self.user_id, "Ori")
        # assign permission to Ori to handle the store's stock
        self.proxy_market.set_stock_manager_perm(self.store_id, self.user_id, "Ori")
        # Ori removes product from store
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, user_id_2, self.prod.getProductId()).getData())
        # check the product isn't in store
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [])

    def test_removeProductNegative(self):
        # the product does not exit
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, -1).isError())
        # now remove a real product from store
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id,
                                                                    self.prod.getProductId()).getData())
        # can't remove a product twice
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id,
                                                                    self.prod.getProductId()).isError())

    def test_removeProductNoManager(self):
        # no such user to remove the product!
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, -1, self.prod.getProductId()).isError())
        # creat a user Ori
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Ori", "1243", "0540000000", 123, 1,  "Israel", "Beer Sheva", "Rager", 1, 0)
        self.user_id_2 = self.proxy_user.login_member(guestId2, "Ori", "1243").getData().getUserID()
        # appoint ori to be a store's manager
        self.proxy_market.appoint_store_manager(self.store_id, self.user_id, "Ori")
        # Ori doesn't have permission to remove the product
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id_2, self.prod.getProductId()).isError())

    def test_removeProductStoreDoestExist(self):
        self.assertTrue(self.proxy_market.remove_product_from_store(-1, self.user_id, self.prod.getProductId()).isError())



if __name__ == '__main__':
    unittest.main()
