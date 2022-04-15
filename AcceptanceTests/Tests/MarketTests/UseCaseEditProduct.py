import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseEditProduct(unittest.TestCase):

    def setUp(self):
        self.proxy = MarketProxyBridge(None)
        self.proxy.add_product(0, "testProduct", 10, "testCategory")

    def test_editProductPricePositive(self):
        self.assertEqual(self.proxy.edit_product_price(0, 20), True)

    def test_editProductNamePositive(self):
        self.assertEqual(self.proxy.edit_product_name(0, "test"), True)

    def test_editProductCategoryPositive(self):
        self.assertEqual(self.proxy.edit_product_price(0, "test"), True)

    def test_editProductDoesntExist(self):
        # the product does not exit
        self.assertEqual(self.proxy.edit_product_price(3, 10), False)
        self.assertEqual(self.proxy.edit_product_name(3, 10), False)
        self.assertEqual(self.proxy.edit_product_category(3, 10), False)

    def test_editProductIncorrectDetails(self):
        self.assertEqual(self.proxy.edit_product_price(0, -10), False)
        self.assertEqual(self.proxy.edit_product_name(0, None), False)
        self.assertEqual(self.proxy.edit_product_category(0, None), False)


if __name__ == '__main__':
    unittest.main()
