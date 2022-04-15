import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseAddProduct(unittest.TestCase):
    def setUp(self):
        self.proxy = MarketProxyBridge(None)

    def test_addProductPositive(self):
        self.assertEqual(self.proxy.add_product(0, "testProduct", 10, "testCategory"), True)

    def test_addProductNegative(self):
        self.assertEqual(self.proxy.add_product(0, "testProduct2", -20, "testCategory"), False)


if __name__ == '__main__':
    unittest.main()
