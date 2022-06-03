import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService
from Backend.Service.Response import Response


class UserCaseRemoveMember(unittest.TestCase):

    def setUp(self):
        self.market_proxy = MarketProxyBridge(MarketRealBridge())
        self.user_proxy = UserProxyBridge(UserRealBridge())
        self.user_proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                                "Ben Gurion", 1, 1).getData()
        self.__guestId_0 = self.user_proxy.login_guest().getData().getUserID()
        self.systemManger = self.user_proxy.login_member(self.__guestId_0, "manager", "1234").getData()

        self.__guestId_1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.member1 = self.user_proxy.login_member(self.__guestId_1, "user1", "1234").getData()

        self.__guestId_2 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.member2 = self.user_proxy.login_member(self.__guestId_2, "user2", "1234").getData()

    def test_removeMember(self):
        self.assertTrue(self.user_proxy.removeMember(self.systemManger.getMemberName(), self.member1.getMemberName()).getData())
        self.assertTrue(self.user_proxy.logout_member(self.member1).isError())

    def test_removeMember_Fail(self):
        self.assertTrue(self.user_proxy.removeMember(self.member2.getMemberName(), self.member2.getMemberName()).isError())
        self.assertTrue(self.user_proxy.removeMember("moshe", self.member2.getMemberName()).isError())

        self.assertTrue(self.user_proxy.removeMember(self.systemManger.getMemberName(), self.member2.getMemberName()).getData())
        self.assertTrue(self.user_proxy.removeMember(self.systemManger.getMemberName(), self.member2.getMemberName()).isError())

    # def tearDown(self):
    #     self.assertTrue(self.user_proxy.removeSystemManger_forTests(self.sm.getMemberName()).getData())




