import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class UseCaseSearchProduct(unittest.TestCase):
    def setUp(self):
        self.market_proxy = MarketProxyBridge(None)
        self.user_proxy = UserProxyBridge(None)
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim", None)
        self.store_id = self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                   0, "000000")
        self.product1 = self.market_proxy.add_product(self.store_id, self.user_id, "Product", 500,
                                                      "Category", ["Test1", "Test2"])
        self.product2 = self.market_proxy.add_product(self.store_id, self.user_id, "Product2", 10,
                                                      "Category2", ["Test3", "Test4"])

    def test_search_by_name(self):
        self.assertEqual(self.market_proxy.search_product_name("Product"), True)
        self.assertEqual(self.market_proxy.search_product_name("Product2"), True)

    def test_search_by_category(self):
        self.assertEqual(self.market_proxy.search_product_category("Category2"), True)

    def test_search_by_price_range(self):
        self.assertEqual(self.market_proxy.search_product_price_range(5, 1000), True)

    def test_search_by_keywords(self):
        self.assertEqual(self.market_proxy.search_product_keyWord("Test1"), True)
        self.assertEqual(self.market_proxy.search_product_keyWord("Test4"), True)

    def test_search_by_name_negative(self):
        self.assertEqual(self.market_proxy.search_product_name("Product3"), False)

    def test_search_by_category_negative(self):
        self.assertEqual(self.market_proxy.search_product_category("Category999"), False)

    def test_search_by_price_range_negative(self):
        self.assertEqual(self.market_proxy.search_product_price_range(2000, 3000), False)

    def test_search_by_keywords_negative(self):
        self.assertEqual(self.market_proxy.search_product_keyWord("Test5"), False)
        self.assertEqual(self.market_proxy.search_product_keyWord(""), False)



if __name__ == '__main__':
    unittest.main()
