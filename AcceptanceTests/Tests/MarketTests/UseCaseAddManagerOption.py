import unittest
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseAddManagerOption(unittest.TestCase):
    def setUp(self):
        self.proxyMarket = MarketProxyBridge(None)
        self.proxyUser = UserProxyBridge(None)
        self.proxyMarket.add_store(0, "testStore")

    def test_addManagerOptionPositive(self):
        self.assertEqual(self.proxyMarket.add_manager_option(0, 0, "testOption"), True)

    def test_addManagerOptionNoStore(self):
        # store doesn't exist
        self.assertEqual(self.proxyMarket.add_manager_option(-1, 0, "testOption"), True)

    def test_addManagerOptionNoManager(self):
        # manager doesn't exist
        self.assertEqual(self.proxyMarket.add_manager_option(0, -1, "testOption"), True)

if __name__ == '__main__':
    unittest.main()
