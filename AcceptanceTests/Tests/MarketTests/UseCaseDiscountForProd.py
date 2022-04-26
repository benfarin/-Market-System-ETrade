import unittest
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseDiscountForProd(unittest.TestCase):
    def setUp(self):
        self.proxy = MarketProxyBridge(None)

    # def test_discountProdPositive(self):
    #     self.assertEqual(self.proxy.discount_prod(0, 0, 20), True)
    #
    # def test_defineDiscountNegative(self):
    #     # store doesn't exist
    #     self.assertEqual(self.proxy.discount_prod(0, -1, 20), False)
    #
    # def test_defineDiscountNegative2(self):
    #     # prod doesn't exist
    #     self.assertEqual(self.proxy.discount_prod(-1, 0, 20), False)
    #
    # def test_defineDiscountNegative3(self):
    #     # discount is negative
    #     self.assertEqual(self.proxy.discount_prod(0, 0, -10), False)


if __name__ == '__main__':
    unittest.main()
