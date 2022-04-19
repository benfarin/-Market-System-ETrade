import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseSearchProduct(unittest.TestCase):
    def setUp(self):
        self.market_proxy = MarketProxyBridge(None)
        self.market_proxy.add_store(0, "TestStore")
        self.market_proxy.add_product(0, 0, "Product1", 10, "Category1")
        self.market_proxy.add_product(1, 0, "Product2", 50, "Category2")

    def test_search_positive1(self):
        self.assertEqual(self.market_proxy.search_product("Product1", "Category1", 0, 20, None, None), True)

    def test_search_positive2(self):
        self.assertEqual(self.market_proxy.search_product("Product2", "Category2", 0, 100, None, None), True)

    def test_search_negative1(self):
        self.assertEqual(self.market_proxy.search_product("Product1", "Category2", 0, 20, None, None), False)

    def test_search_negative2(self):
        self.assertEqual(self.market_proxy.search_product("Product2", "Category1", 0, 20, None, None), False)

    def test_search_negative3(self):
        self.assertEqual(self.market_proxy.search_product("Product1", "Category1", 50, 100, None, None), False)

    def tearDown(self):
        self.market_proxy.remove_product(0, 0)
        self.market_proxy.close_store(0)



if __name__ == '__main__':
    unittest.main()
