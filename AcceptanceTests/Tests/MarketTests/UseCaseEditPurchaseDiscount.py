import unittest
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseEditPurchaseDiscount(unittest.TestCase):
    def setUp(self):
        self.proxyMarket = MarketProxyBridge(None)
        self.proxyUser = UserProxyBridge(None)
        self.proxyMarket.add_store(0, "testStore")

    def test_EditPurchasePositive(self):
        self.assertEqual(self.proxyMarket.edit_purchase(0, "testPurchase"), True)

    def test_EditDiscountPositive(self):
        self.assertEqual(self.proxyMarket.edit_discount(0, 10), True)

    def test_EditPurchaseNegative(self):
        # store doesn't exist
        self.assertEqual(self.proxyMarket.edit_purchase(-1, "testPurchase"), False)

    def test_EditDiscountNegative(self):
        # discount is negative
        self.assertEqual(self.proxyMarket.edit_discount(0, -10), False)


if __name__ == '__main__':
    unittest.main()
