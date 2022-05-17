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
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser", "1234", "0540000000", 123,[] ,"Israel", "Beer Sheva", "Rager", 1, "testBank")
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.user_id = self.proxy_user.login_member(self.__guestId1, "testUser", "1234").getData().getUserID()
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()
        # store_id, user_id, name, price, category, key_words
        self.prod_id = self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10,
                                                              "testCategory", 10,  ["testKeyWord"]).getData()

    def test_editProductPricePositive(self):
        # store_id, user_id, prod_id, new_price
        product = self.proxy_market.edit_product_price(self.store_id, self.user_id, self.prod_id.getProductId(), 20).getData()
        self.assertTrue(product.getProductPrice(), 20)

    def test_editProductNamePositive(self):
        product = self.proxy_market.edit_product_name(self.user_id, self.store_id, self.prod_id.getProductId(), "newName").getData()
        self.assertTrue(product.getProductName(), "newName")

    def test_editProductCategoryPositive(self):
        product = self.proxy_market.edit_product_category(self.user_id, self.store_id, self.prod_id.getProductId(),
                                                    "newCategory").getData()
        self.assertTrue(product.getProductCategory(), "newCategory")

    def test_editProductWeightPositive(self):
        product = self.proxy_market.edit_product_Weight(self.user_id, self.store_id, self.prod_id.getProductId(), 20).getData()
        self.assertTrue(product.getProductWeight(), 20)

    def test_editProduct_Fail(self):
        # the store doesn't exist
        self.assertTrue(self.proxy_market.edit_product_price(-10, self.user_id, self.prod_id.getProductId(), 10).isError())
        self.assertTrue(self.proxy_market.edit_product_name(self.user_id, -1, self.prod_id.getProductId(), "newName").isError())
        self.assertTrue(self.proxy_market.edit_product_category(self.user_id, -1, self.prod_id.getProductId(), "newCategory").isError())
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, self.user_id, self.prod_id.getProductId(), -3).isError())
        self.assertTrue(self.proxy_market.edit_product_price(self.store_id, -1, self.prod_id.getProductId(), 10).isError())


if __name__ == '__main__':
    unittest.main()
