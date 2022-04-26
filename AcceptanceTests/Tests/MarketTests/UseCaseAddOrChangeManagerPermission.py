import unittest
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge


class UseCaseAddOrChangeManagerPermission(unittest.TestCase):
    # use-case 5.1 actions according to permissions

    def setUp(self):
        self.proxy_market = MarketProxyBridge(None)
        self.proxy_user = UserProxyBridge(None)
        self.proxy_user.open_store("testStore", 0, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000)

    def test_addManagerOptionPositive(self):
        self.assertEqual(self.proxy_market.add_manager_option(0, 0, "testOption"), True)

    def test_addManagerOptionNoStore(self):
        # store doesn't exist
        self.assertEqual(self.proxy_market.add_manager_option(-1, 0, "testOption"), True)

    def test_addManagerOptionNoManager(self):
        # manager doesn't exist
        self.assertEqual(self.proxy_market.add_manager_option(0, -1, "testOption"), True)


if __name__ == '__main__':
    unittest.main()
