import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseSearchProduct(unittest.TestCase):
    def setUp(self):
        self.market_proxy = MarketProxyBridge(MarketRealBridge())
        self.user_proxy = UserProxyBridge(UserRealBridge())
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim")
        self.user_proxy.login_member("user1", "1234")
        self.store_id = self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                   0, 1)
        self.product1 = self.market_proxy.add_product_to_store(self.store_id, self.user_id, "Product", 500,
                                                      "Category", ["Test1", "Test2"])
        self.product2 = self.market_proxy.add_product_to_store(self.store_id, self.user_id, "Product2", 10,
                                                      "Category2", ["Test3", "Test4"])

    def test_search_by_name(self):
        self.assertEqual(self.market_proxy.search_product_name("Product"), [self.product1])
        self.assertEqual(self.market_proxy.search_product_name("Product2"), [self.product2])

    def test_search_by_category(self):
        self.assertEqual(self.market_proxy.search_product_category("Category2"), [self.product2])

    def test_search_by_price_range(self):
        self.assertEqual(self.market_proxy.search_product_price_range(5, 1000), [self.product1, self.product2])

    def test_search_by_keywords(self):
        self.assertEqual(self.market_proxy.search_product_keyWord("Test1"), [self.product1])
        self.assertEqual(self.market_proxy.search_product_keyWord("Test4"), [self.product2])

    def test_search_by_name_negative(self):
        self.assertEqual(self.market_proxy.search_product_name("Product3"), [])

    def test_search_by_category_negative(self):
        self.assertEqual(self.market_proxy.search_product_category("Category999"), [])

    def test_search_by_price_range_negative(self):
        self.assertEqual(self.market_proxy.search_product_price_range(2000, 3000), [])

    def test_search_by_keywords_negative(self):
        self.assertEqual(self.market_proxy.search_product_keyWord("Test5"), [])
        self.assertEqual(self.market_proxy.search_product_keyWord(""), [])



if __name__ == '__main__':
    unittest.main()
