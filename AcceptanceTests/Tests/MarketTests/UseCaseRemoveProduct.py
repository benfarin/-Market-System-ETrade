import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseRemoveProduct(unittest.TestCase):

    def setUp(self):
        self.proxy = MarketProxyBridge(None)
        self.proxy.add_product(0, "testProduct", 10, "testCategory")

    def test_removeProductPositive(self):
        self.assertEqual(self.proxy.remove_product(0), True)

    def test_removeProductNegative(self):
        # the product does not exit
        self.assertEqual(self.proxy.remove_product(3), False)


if __name__ == '__main__':
    unittest.main()
