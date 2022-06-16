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
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "manager", "1234")
        # create 2 users
        self.__guestId_1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("Kfir", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.member1 = self.user_proxy.login_member(self.__guestId_1, "Kfir", "1234").getData()

        self.__guestId_2 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("Niv", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.member2 = self.user_proxy.login_member(self.__guestId_2, "Niv", "1234").getData()

    def tearDown(self) -> None:
        self.user_proxy.removeMember("manager","Niv")
        self.user_proxy.removeMember("manager", "Kfir")
        self.user_proxy.removeSystemManger_forTests("manager")

    def test_removeMember(self):
        self.assertTrue(self.user_proxy.removeMember("manager", "Kfir").getData())
        self.assertTrue(self.user_proxy.removeMember("manager", "Niv").getData())
        # user that was removed should be able to logout
        self.assertTrue(self.user_proxy.logout_member(self.member1).isError())

    def test_removeMember_permission(self):
        # Kfir is not a system manager
        self.assertTrue(self.user_proxy.removeMember("Kfir", "Niv").isError())
        # Ori doesn't exist in the system
        self.assertTrue(self.user_proxy.removeMember("Ori", "Niv").isError())
        self.assertTrue(self.user_proxy.removeMember("manager", "Ori").isError())

        # can't remove a member twice!
        self.assertTrue(self.user_proxy.removeMember("manager", "Kfir").getData())
        self.assertTrue(self.user_proxy.removeMember("manager", "Kfir").isError())

    def test_remove_member_threaded(self):
        # one of them should be an error - because you can't remove a member twice
        t1 = ThreadWithReturn(target=self.user_proxy.removeMember, args =("manager","Kfir"))
        t2 = ThreadWithReturn(target=self.user_proxy.removeMember, args=("manager", "Kfir"))
        t1.start()
        t2.start()
        ans1 = t1.join()
        ans2 = t2.join()
        self.assertTrue((ans1.isError() or ans2.isError()) and (ans1.getData() or ans2.getData()))






