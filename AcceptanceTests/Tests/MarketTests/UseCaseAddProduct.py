import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseAddProduct(unittest.TestCase):
    def setUp(self):
        self.proxy = MarketProxyBridge(None)
        self.proxy.add_store(0, "testStore")

    def test_addProductPositive(self):
        #id , store_id, name, category
        self.assertEqual(self.proxy.add_product(0, 0, "testProduct", 10, "testCategory"), True)

    def test_addProductNegative(self):
        self.assertEqual(self.proxy.add_product(0, 0, "testProduct2", -20, "testCategory"), False)


if __name__ == '__main__':
    unittest.main()
