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
        admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(admin_id, "Manager", "1234")

        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Bar", "1243", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.user_id = self.proxy_user.login_member(self.__guestId1, "Bar", "1243").getData().getUserID()
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, 1, "Israel", "Beer Sheva",
                                                   "Rager", 1, 00000).getData().getStoreId()
        # store_id, user_id, name, price, category, key_words
        self.prod = self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10,
                                                           "testCategory", 10, ["testKeyWord"]).getData()
        self.proxy_market.add_quantity_to_store(self.store_id, self.user_id, self.prod.getProductId(), 100)

    def tearDown(self) -> None:
        self.proxy_user.removeMember("Manager", "Bar")
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_removeProductPositive(self):
        # store_id, user_id, prod_id
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [self.prod.getProductId()])

        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId()).getData())
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [])
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)

    def test_removeProductByManagerWithPermission(self):
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Ori", "1243", "0540000000", 123, 1, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.user_id_2 = self.proxy_user.login_member(guestId2, "Ori", "1243").getData().getUserID()
        self.proxy_market.appoint_store_manager(self.store_id, self.user_id, "Ori")
        self.proxy_market.set_stock_manager_perm(self.store_id, self.user_id, "Ori")

        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id_2, self.prod.getProductId()).getData())
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [])

        # tear down!
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)
        self.proxy_user.removeMember("Manager", "Ori")

    def test_removeProductNegative(self):
        # the product does not exit
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, -1).isError())
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)

    def test_removeProductNoManager(self):
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, -1, self.prod.getProductId()).isError())
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Ori", "1243", "0540000000", 123, 1,  "Israel", "Beer Sheva", "Rager", 1, 0)
        self.user_id_2 = self.proxy_user.login_member(guestId2, "Ori", "1243").getData().getUserID()
        self.proxy_market.appoint_store_manager(self.store_id, self.user_id, "Ori")
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id_2, self.prod.getProductId()).isError())
        # tear down!
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)
        self.proxy_user.removeMember("Manager", "Ori")

    def test_removeProductStoreDoestExist(self):
        self.assertTrue(self.proxy_market.remove_product_from_store(-3, self.user_id, self.prod.getProductId()).isError())
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)

    def test_removeProductTwice(self):
        # remove product that was already already removed
        self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId())
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId()).isError())
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)



if __name__ == '__main__':
    unittest.main()
