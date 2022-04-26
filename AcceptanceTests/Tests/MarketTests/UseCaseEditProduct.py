import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MarketService import MarketService
from Service.UserService import UserService


class UseCaseEditProduct(unittest.TestCase):
    # use-case 4.1.3

    def setUp(self):
        self.proxy_market = MarketProxyBridge(MarketService())
        self.proxy_user = UserProxyBridge(UserRealBridge(UserService(), MarketService()))
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.user_id = self.proxy_user.register("testUser", "1243", "0540000000", 123,[] ,"Israel", "Beer Sheva", "Rager", 1, "testBank", None)
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000)
        # store_id, user_id, name, price, category, key_words
        self.prod_id = self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, "testCategory", ["testKeyWord"])

    def test_editProductPricePositive(self):
        # store_id, user_id, prod_id, new_price
        self.assertEqual(self.proxy_market.edit_product_price(self.store_id, self.user_id, self.prod_id, 20), True)

    # def test_editProductNamePositive(self):
    #     self.assertEqual(self.proxy.edit_product_name(0, 0, "test"), True)

    # def test_editProductCategoryPositive(self):
    #     self.assertEqual(self.proxy.edit_product_price(0, 0, "test"), True)

    def test_editProductStoreDoesntExists(self):
        # the store doesn't exist
        self.assertEqual(self.proxy_market.edit_product_price(-10, self.user_id, self.prod_id, 10), False)
        # self.assertEqual(self.proxy.edit_product_name(0, 0, None), False)
        # self.assertEqual(self.proxy.edit_product_category(0, 0, None), False)

    def test_editProductNoManager(self):
        # the manager's ID is negative
        self.assertEqual(self.proxy_market.edit_product_price(self.store_id, -1, self.prod_id, 10), False)

    def test_editProductDoesntExists(self):
        # the product doesn't exists
        self.assertEqual(self.proxy_market.edit_product_price(self.store_id, self.user_id, -1, 10), False)
        # self.assertEqual(self.proxy.edit_product_name(0, 3, 10), False)
        # self.assertEqual(self.proxy.edit_product_category(0, 3, 10), False)

    def test_editProductNegativePrice(self):
        # the new price is negative
        self.assertEqual((self.proxy_market.edit_product_price(self.store_id, self.user_id, self.prod_id, -3)), False)

    def tearDown(self):
        self.proxy_market.close_store(self.store_ids)


if __name__ == '__main__':
    unittest.main()
