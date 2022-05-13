import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseMemberLogout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_proxy = UserProxyBridge(UserRealBridge())
        cls.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        cls.user_proxy.login_member("Manager", "1234")
        cls.__guestId1 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register(cls.__guestId1, "user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim")

    def test_logout_positive1(self):
        self.user_proxy.login_member("user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1"))

    def test_logout_negative1(self):
        self.assertRaises(Exception, self.user_proxy.logout_member("User1").getError())

    def test_logout_negative2(self):
        self.user_proxy.login_member("user1", "1234")
        self.assertRaises(Exception, self.user_proxy.logout_member(-999))

    def test_remove_member(self):
        print(self.user_proxy.removeMember("Manager", "user1").getData())
        print(self.user_proxy.login_member("user1", "1234").getError())



if __name__ == '__main__':
    unittest.main()
