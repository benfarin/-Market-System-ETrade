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

        cls.guest_id = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, "HaPoalim")

        cls.__guestId1 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, "HaPoalim")

    def test_logout_positive1(self):
        self.user_proxy.login_member(self.guest_id, "user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1").getData())

    def test_logout_negative2(self):
        self.assertTrue(self.user_proxy.logout_member(-999).isError())


if __name__ == '__main__':
    unittest.main()
