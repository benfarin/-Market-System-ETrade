import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseEditProduct(unittest.TestCase):
    # use-case 4.1.3
    databases = {'testing'}
    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign manager
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "Manager", "1234")
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Bar", "1234", "0540000000", 123, 1 ,"Israel", "Beer Sheva", "Rager", 1, 0)
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.user_id = self.proxy_user.login_member(self.__guestId1, "Bar", "1234").getData().getUserID()
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, 1, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()
        # store_id, user_id, name, price, category, key_words
        self.prod_id = self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10,
                                                              "testCategory", 10,  ["testKeyWord"]).getData()

    def tearDown(self):
        self.proxy_user.exit_system(self.admin_id)
        self.proxy_user.exit_system(self.__guestId1)
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)
        self.proxy_user.removeMember("Manager", "Bar")
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_editProductPricePositive(self):
        # store_id, user_id, prod_id, new_price
        product = self.proxy_market.edit_product_price(self.user_id, self.store_id, self.prod_id.getProductId(), 20).getData()
        p = self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().get(self.prod_id.getProductId())
        self.assertEqual(20, product.getProductPrice())
        self.assertEqual(20, p.getProductPrice())

    def test_editProductNamePositive(self):
        product = self.proxy_market.edit_product_name(self.user_id, self.store_id, self.prod_id.getProductId(), "newName").getData()
        p = self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().get(self.prod_id.getProductId())
        self.assertEqual("newName", product.getProductName())
        self.assertEqual("newName", p.getProductName())

    def test_editProductCategoryPositive(self):
        product = self.proxy_market.edit_product_category(self.user_id, self.store_id, self.prod_id.getProductId(),
                                                          "newCategory").getData()
        p = self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().get(self.prod_id.getProductId())
        self.assertEqual("newCategory", product.getProductCategory())
        self.assertEqual("newCategory", p.getProductCategory())

    def test_editProductWeightPositive(self):
        product = self.proxy_market.edit_product_Weight(self.user_id, self.store_id, self.prod_id.getProductId(), 20).getData()
        p = self.proxy_market.get_store_by_ID(self.store_id).getData().getProducts().get(self.prod_id.getProductId())
        self.assertEqual(20, product.getProductWeight())
        self.assertEqual(20, p.getProductWeight())

    def test_editProductUserDoesntExists(self):
        # the store doesn't exist
        self.assertTrue(self.proxy_market.edit_product_price(-10, self.user_id, self.prod_id.getProductId(), 10).isError())

    def test_editProductStoreDoesntExists(self):
        self.assertTrue(self.proxy_market.edit_product_name(self.user_id, 10, self.prod_id.getProductId(), "newName").isError())

    def test_editProductDoesntExists(self):
        self.assertTrue(self.proxy_market.edit_product_category(self.user_id, 7, self.prod_id.getProductId(), "newCategory").isError())

    def test_editProductNegativePriceOrWeight(self):
        # the new price is negative
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, self.user_id, self.prod_id.getProductId(), -3).isError())
        self.assertTrue(self.proxy_market.edit_product_Weight(self.store_id, self.user_id, self.prod_id.getProductId(), -3).isError())


if __name__ == '__main__':
    unittest.main()
