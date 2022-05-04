import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MarketService
from Service.UserService import UserService


class UseCaseRemoveProduct(unittest.TestCase):

    def setUp(self):
        self.proxy_market = MarketProxyBridge(MarketRealBridge(MarketService()))
        self.proxy_user = UserProxyBridge(UserRealBridge(UserService(), MarketService()))
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.user_id = self.proxy_user.register("testUser", "1243", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank", None)
        self.proxy_user.login_member("testUser", "1243")
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva","Rager", 1, 00000)
        # store_id, user_id, name, price, category, key_words
        self.prod = self.proxy_market.add_product_to_store(self.store_id, self.user_id, "testProduct", 10, "testCategory", ["testKeyWord"])
        self.proxy_market.add_quantity_to_store(self.store_id, self.user_id, self.prod.getProductId(), 100)


    def test_removeProductPositive(self):
        # store_id, user_id, prod_id
        self.assertEqual(self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId()), True)

    def test_removeProductNegative(self):
        # the product does not exit
        self.assertRaises(Exception, self.proxy_market.remove_product_from_store(self.store_id, self.user_id, -1))

    def test_removeProductNoManager(self):
        # the product does not exit
        self.assertRaises(Exception, self.proxy_market.remove_product_from_store(self.store_id, -1, self.prod.getProductId()))

    def test_removeProductStoreDoestExist(self):
        # the product does not exit
        self.assertRaises(Exception, self.proxy_market.remove_product_from_store(-3, self.user_id, self.prod.getProductId()))

    def test_removeProductTwice(self):
        # remove product that was already already removed
        self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId())
        self.assertRaises(Exception, self.proxy_market.remove_product_from_store(self.store_id, self.user_id, self.prod.getProductId()))


if __name__ == '__main__':
    unittest.main()
