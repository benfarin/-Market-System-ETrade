import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MarketService import MarketService
from Service.UserService import UserService


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.proxy = UserProxyBridge(UserRealBridge(UserService(), MarketService()))
        self.proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)

    def test_login(self):
        try:
            self.proxy.login_guest()
            self.assertTrue(True)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
