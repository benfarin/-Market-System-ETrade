import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MarketService import MarketService
from Service.UserService import UserService


class UseCaseRemoveProduct(unittest.TestCase):

    def setUp(self):
        self.proxy_market = MarketProxyBridge(MarketService())
        self.proxy_user = UserProxyBridge(UserRealBridge(UserService(), MarketService()))
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.user_id = self.proxy_user.register("testUser", "1243", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank", None)
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva","Rager", 1, 00000)
        # store_id, user_id, name, price, category, key_words
        self.prod_id = self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10,"testCategory", ["testKeyWord"])


    def test_removeProductPositive(self):
        # store_id, user_id, prod_id
        self.assertEqual(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod_id), True)

    def test_removeProductNegative(self):
        # the product does not exit
        self.assertEqual(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, -1), False)

    def test_removeProductNoManager(self):
        # the product does not exit
        self.assertEqual(self.proxy_market.remove_product_from_store(self.store_id, -1, self.prod_id), False)

    def test_removeProductStoreDoestExist(self):
        # the product does not exit
        self.assertEqual(self.proxy_market.remove_product_from_store(-3, self.user_id, self.prod_id), False)

    def tearDown(self):
        self.proxy_market.close_store(self.store_id)


if __name__ == '__main__':
    unittest.main()
