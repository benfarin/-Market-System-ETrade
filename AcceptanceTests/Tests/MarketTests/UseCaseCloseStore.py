import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseCloseStore(unittest.TestCase):
    def setUp(self):
        self.proxy = MarketProxyBridge(None)
        self.proxy.add_store(0, "testStore")

    def test_closeStorePositive(self):
        self.assertEqual(self.proxy.close_store(0), True)

    def test_closeStoreNegative(self):
        # store doesn't exist
        self.assertEqual(self.proxy.close_store(-1), False)

if __name__ == '__main__':
    unittest.main()
