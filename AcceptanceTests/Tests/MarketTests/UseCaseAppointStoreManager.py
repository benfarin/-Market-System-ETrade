import unittest
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseAppointStoreManager(unittest.TestCase):
    def setUp(self):
        self.proxyMarket = MarketProxyBridge(None)
        self.proxyUser = UserProxyBridge(None)
        self.proxyMarket.add_store(0, "testStore")

    def test_AppointStoreManagerPositive(self):
        self.assertEqual(self.proxyMarket.appoint_store_manager(0, 0), True)

    def test_AppointStoreManagerNoStore(self):
        self.assertEqual(self.proxyMarket.appoint_store_manager(-1, 0), False)

    def test_AppointStoreManagerNoOwner(self):
        self.assertEqual(self.proxyMarket.appoint_store_manager(0,-1), False)

if __name__ == '__main__':
    unittest.main()
