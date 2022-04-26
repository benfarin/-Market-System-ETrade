import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class UseCaseAddProduct(unittest.TestCase):
    # use-case 4.1.1

    def setUp(self):
        self.proxy_market = MarketProxyBridge(None)
        self.proxy_user = UserProxyBridge(None)

        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.user_id = self.proxy_user.register("testUser", "1243", "0540000000", 123,[] ,"Israel", "Beer Sheva", "Rager", 1, "testBank", None)
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000)

    def test_addProductPositive(self):
        # store_id, user_id, name, price, category, key_words
        self.assertEqual(self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, "testCategory", ["test"]), True)

    def test_addProductNegativePrice(self):
        # price is negative
        self.assertEqual(self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", -20, "testCategory", ["test"]), False)

    def test_addProductNoKeyWord(self):
        # no key-word
        self.assertEqual(self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, "testCategory", []), False)

    def test_addProductNoCategory(self):
        # no category
        self.assertEqual(self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, None, ["test"]), False)

    def test_addProductIllegalStoreId(self):
        # illegal store id
        self.assertEqual(self.proxy_market.add_product_to_store(-1, self.user_id, "testProduct", 10, "testCategory", ["test"]), False)

    def test_addProductIllegalUserId(self):
        # illegal user id
        self.assertEqual(self.proxy_market.add_product_to_store(self.store_id, -1, "testProduct", 10, "testCategory", ["test"]), False)

    def tearDown(self):
        self.proxy_market.close_store(self.store_id)


if __name__ == '__main__':
    unittest.main()
