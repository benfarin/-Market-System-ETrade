import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UserCaseRemoveMember(unittest.TestCase):

    market_proxy = MarketProxyBridge(MarketRealBridge())
    user_proxy = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign system manager
        self.user_proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(admin_id, "manager", "1234")

        self.__guestId_1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.member1 = self.user_proxy.login_member(self.__guestId_1, "user1", "1234").getData()

        self.__guestId_2 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.member2 = self.user_proxy.login_member(self.__guestId_2, "user2", "1234").getData()

    def tearDown(self) -> None:
        self.user_proxy.removeSystemManger_forTests("manager")

    def test_removeMember(self):
        self.assertTrue(self.user_proxy.removeMember("manager", "user1").getData())
        self.assertTrue(self.user_proxy.removeMember("manager", "user2").getData())
        # user that was removed should be able to logout
        self.assertTrue(self.user_proxy.logout_member(self.member1).isError())

    def test_removeMember_permission(self):
        self.assertTrue(self.user_proxy.removeMember("user2", "user1").isError())
        self.assertTrue(self.user_proxy.removeMember("Ori", "user1").isError())
        # not a member
        self.assertTrue(self.user_proxy.removeMember("manager", "Ori").isError())

        # can't remove a member twice!
        self.assertTrue(self.user_proxy.removeMember("manager", "user2").getData())
        self.assertTrue(self.user_proxy.removeMember("manager", "user2").isError())

        self.assertTrue(self.user_proxy.removeMember("manager", "user1").getData())

    def test_remove_member_threaded(self):
        t1 = ThreadWithReturn(target=self.user_proxy.removeMember, args =("manager","user2"))
        t2 = ThreadWithReturn(target=self.user_proxy.removeMember, args=("manager", "user2"))
        t1.start()
        t2.start()
        ans1 = t1.join()
        ans2 = t2.join()
        self.assertTrue(ans1.isError() or ans2.isError())
        self.assertTrue(self.user_proxy.removeMember("manager", "user1").getData())






