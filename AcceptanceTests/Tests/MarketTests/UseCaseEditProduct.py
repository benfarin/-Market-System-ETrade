import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseEditProduct(unittest.TestCase):
    # use-case 4.1.3
    @classmethod
    def setUpClass(self):

        self.proxy_market = MarketProxyBridge(MarketRealBridge())
        self.proxy_user = UserProxyBridge(UserRealBridge())

        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserId()
        self.proxy_user.register(self.__guestId1, "testUser", "1234", "0540000000", 123,[] ,"Israel", "Beer Sheva", "Rager", 1, "testBank")
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.user_id = self.proxy_user.login_member("testUser", "1234").getData().getUserID()
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()
        # store_id, user_id, name, price, category, key_words
        self.prod_id = self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, "testCategory", ["testKeyWord"]).getData()

    def test_editProductPricePositive(self):
        # store_id, user_id, prod_id, new_price
        try:
            self.proxy_market.edit_product_price(self.store_id, self.user_id, self.prod_id.getProductId(), 20).getData()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_editProductNamePositive(self):
        try:
            self.proxy_market.edit_product_name(self.user_id, self.store_id, self.prod_id.getProductId(), "newName")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_editProductCategoryPositive(self):
        try:
            self.proxy_market.edit_product_category(self.user_id, self.store_id, self.prod_id.getProductId(),
                                                    "newCategory")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_editProductStoreDoesntExists(self):
        # the store doesn't exist
        self.assertTrue(self.proxy_market.edit_product_price(-10, self.user_id, self.prod_id.getProductId(), 10).isError())
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1234")
        self.assertTrue(self.proxy_market.edit_product_price(-10, self.user_id, self.prod_id.getProductId(), 10).isError())


    def test_editProductStoreDoesntExists2(self):
        self.assertTrue(self.proxy_market.edit_product_name(self.user_id, -1, self.prod_id.getProductId(), "newName").isError())
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1234")
        self.assertTrue(self.proxy_market.edit_product_name(self.user_id, -1, self.prod_id.getProductId(), "newName").isError())



    def test_editProductStoreDoesntExists3(self):
        self.assertTrue(self.proxy_market.edit_product_category(self.user_id, -1, self.prod_id.getProductId(), "newCategory").isError())
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1234")
        self.assertTrue(self.proxy_market.edit_product_category(self.user_id, -1, self.prod_id.getProductId(), "newCategory").isError())


    def test_editProductNoManager(self):
        # the manager's ID is negative
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, -1, self.prod_id.getProductId(), 10).isError())
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1234")
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, -1, self.prod_id.getProductId(), 10).isError())


    def test_editProductDoesntExists(self):
        # the product doesn't exists
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, self.user_id, -1, 10).isError())
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1234")
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, self.user_id, -1, 10).isError())
        # self.assertEqual(self.proxy.edit_product_name(0, 3, 10), False)
        # self.assertEqual(self.proxy.edit_product_category(0, 3, 10), False)

    def test_editProductNegativePrice(self):
        # the new price is negative
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, self.user_id, self.prod_id.getProductId(), -3).isError())
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1234")
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, self.user_id, self.prod_id.getProductId(), -3).isError())



if __name__ == '__main__':
    unittest.main()
