import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.user_proxy = UserProxyBridge(UserRealBridge(UserService(), MemberService()))
        self.market_proxy = MarketProxyBridge(MarketProxyBridge(MemberService()))
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim")
        self.user_proxy.login_member("user1", "1234")

    def test_open_store_positive1(self):
        self.assertTrue(self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000"), 1)


    def test_open_store_negative1(self):
        self.assertRaises(Exception, self.user_proxy.open_store("store", -999, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                   0, "000000"))



if __name__ == '__main__':
    unittest.main()
