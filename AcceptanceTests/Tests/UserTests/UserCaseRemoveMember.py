import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService
from Backend.Service.Response import Response


class UserCaseRemoveMember(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.market_proxy = MarketProxyBridge(MarketRealBridge())
        cls.user_proxy = UserProxyBridge(UserRealBridge())
        cls.sm = cls.user_proxy.appoint_system_manager("user1", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                                         "Ben Gurion", 1, 1).getData()
        cls.__guestId_1 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register(cls.__guestId_1, "user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, "HaPoalim")
        cls.member1 = cls.user_proxy.login_member("user1", "1234").getData()

        cls.__guestId_2 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register(cls.__guestId_2, "user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, "HaPoalim")
        cls.member2 = cls.user_proxy.login_member("user2", "1234").getData()

    def test_removeMember(self):
        self.assertTrue(self.user_proxy.removeMember(self.sm.getMemberName(), self.member1.getMemberName()).getData())
        self.assertTrue(self.user_proxy.logout_member(self.member1).isError())

    def test_removeMember_Fail(self):
        self.assertTrue(self.user_proxy.removeMember(self.member2.getMemberName(), self.member2.getMemberName()).isError())
        self.assertTrue(self.user_proxy.removeMember("moshe", self.member2.getMemberName()).isError())

        self.assertTrue(self.user_proxy.removeMember(self.sm.getMemberName(), self.member2.getMemberName()).getData())
        self.assertTrue(self.user_proxy.removeMember(self.sm.getMemberName(), self.member2.getMemberName()).isError())



