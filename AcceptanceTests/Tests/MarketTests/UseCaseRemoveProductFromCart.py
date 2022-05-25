import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseRemoveProduct(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.proxy_market = MarketProxyBridge(MarketRealBridge())
        cls.proxy_user = UserProxyBridge(UserRealBridge())
        cls.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        cls.__guestId1 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser", "1243", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1,
                                 "testBank")
        cls.user_id = cls.proxy_user.login_member(cls.__guestId1, "testUser", "1243").getData().getUserID()
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        cls.store_id = cls.proxy_user.open_store("testStore", cls.user_id, 123, None, "Israel", "Beer Sheva",
                                                   "Rager", 1, 00000).getData().getStoreId()
        # store_id, user_id, name, price, category, key_words
        cls.prod = cls.proxy_market.add_product_to_store(cls.store_id, cls.user_id, "testProduct", 10,
                                                           "testCategory", 10, ["testKeyWord"]).getData()
        cls.proxy_market.add_quantity_to_store(cls.store_id, cls.user_id, cls.prod.getProductId(), 100)

    def test_removeProductPositive(self):
        # store_id, user_id, prod_id
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [self.prod.getProductId()])

        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId()).getData())
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [])

    def test_removeProductByManagerWithPermission(self):
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "1243", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1,
                                 "testBank")
        self.user_id_2 = self.proxy_user.login_member(guestId2, "testUser2", "1243").getData().getUserID()
        self.proxy_market.appoint_store_manager(self.store_id, self.user_id, "testUser2")
        self.proxy_market.set_stock_manager_perm(self.store_id, self.user_id, "testUser2")

        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id_2, self.prod.getProductId()).getData())
        storeProductsIds = [pId for pId in self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().keys()]
        self.assertEqual(storeProductsIds, [])

    def test_removeProductNegative(self):
        # the product does not exit
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, -1).isError())

    def test_removeProductNoManager(self):
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, -1, self.prod.getProductId()).isError())
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "1243", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1,
                                "testBank")
        self.user_id_2 = self.proxy_user.login_member(guestId2, "testUser2", "1243").getData().getUserID()
        self.proxy_market.appoint_store_manager(self.store_id, self.user_id, "testUser2")
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id_2, self.prod.getProductId()).isError())

    def test_removeProductStoreDoestExist(self):
        self.assertTrue(self.proxy_market.remove_product_from_store(-3, self.user_id, self.prod.getProductId()).isError())

    def test_removeProductTwice(self):
        # remove product that was already already removed
        self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId())
        self.assertTrue(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId()).isError())


if __name__ == '__main__':
    unittest.main()
