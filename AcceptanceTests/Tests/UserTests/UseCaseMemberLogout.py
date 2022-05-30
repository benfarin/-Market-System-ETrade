import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService


class UseCaseMemberLogout(unittest.TestCase):
    #usecase 3.1
    @classmethod
    def setUpClass(cls):
        cls.user_proxy = UserProxyBridge(UserRealBridge())
        cls.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                              "Ben Gurion", 1, 1)

        cls.__guestId1 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, "HaPoalim")

    def test_logout_positive(self):
        self.user_proxy.login_member(self.__guestId1, "user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1").getData())

    def test_logout_systemManger(self):
        self.assertTrue(self.user_proxy.logout_member("Manager").isError())

        guestId = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(guestId, "Manager", "1234")
        self.assertTrue(self.user_proxy.logout_member("Manager").getData())

    def test_logout_login_logout(self):
        self.user_proxy.login_member(self.__guestId1, "user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1").getData())

        self.__guestId1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.__guestId1, "user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1").getData())

    def test_logout_FAIL(self):
        user_id = self.user_proxy.login_member(self.__guestId1, "user1", "1234").getData().getUserID()

        self.assertTrue(self.user_proxy.logout_member("no user").isError())

        self.user_proxy.logout_member(user_id)
        self.assertTrue(self.user_proxy.logout_member(user_id).isError())


if __name__ == '__main__':
    unittest.main()
