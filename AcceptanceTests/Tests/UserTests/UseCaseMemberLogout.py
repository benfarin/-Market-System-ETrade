import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseMemberLogout(unittest.TestCase):
    def setUp(self):
        self.user_proxy = UserProxyBridge(UserRealBridge(UserService(), MemberService()))
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim")

    def test_logout_positive1(self):
        self.user_proxy.login_member("user1", "1234")
        self.assertEqual(self.user_proxy.logout_member("user1"), True)

    def test_logout_negative1(self):
        self.assertRaises(Exception, self.user_proxy.logout_member("User1"))

    def test_logout_negative2(self):
        self.user_proxy.login_member(self.user_id, "1234")
        self.assertRaises(Exception, self.user_proxy.logout_member(-999))


if __name__ == '__main__':
    unittest.main()
