import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MarketService import MarketService
from Service.UserService import UserService


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.proxy = UserProxyBridge(UserRealBridge(UserService(), MarketService()))
        self.proxy.

    def test_login(self):
        self.assertEqual(self.proxy.login_guest(), True)


if __name__ == '__main__':
    unittest.main()
