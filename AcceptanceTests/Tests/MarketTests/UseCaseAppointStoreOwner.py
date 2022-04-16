import unittest
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseAppointStoreOwner(unittest.TestCase):
    def setUp(self):
        self.proxyMarket = MarketProxyBridge(None)
        self.proxyUser = UserProxyBridge(None)
        self.proxyMarket.add_store(0, "testStore")

    def test_AppointStoreOwnerPositive(self):
        self.assertEqual(self.proxyMarket.appoint_store_owner(0, 0), True)

    def test_AppointStoreOwnerNoStore(self):
        self.assertEqual(self.proxyMarket.appoint_store_owner(-1, 0), False)

    def test_AppointStoreOwnerNoOwner(self):
        self.assertEqual(self.proxyMarket.appoint_store_owner(0,-1), False)

if __name__ == '__main__':
    unittest.main()
