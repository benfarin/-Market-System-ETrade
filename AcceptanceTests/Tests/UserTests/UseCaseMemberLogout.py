import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService


class UseCaseMemberLogout(unittest.TestCase):
    #usecase 3.1
    user_proxy = UserProxyBridge(UserRealBridge())

    def setUp(self):
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                              "Ben Gurion", 1, 1)
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "Manager", "1234")
        self.__guestId1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva", "Ben Gurion", 0, 0)

    def tearDown(self) -> None:
        self.user_proxy.exit_system(self.admin_id)
        self.user_proxy.exit_system(self.__guestId1)
        self.user_proxy.removeMember("Manager", "user1")
        self.user_proxy.removeSystemManger_forTests("Manager")
        self.user_proxy.reset_management()

    def test_logout_positive(self):
        self.user_proxy.login_member(self.__guestId1, "user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1").getData())

    def test_logout_systemManger(self):
        self.assertTrue(self.user_proxy.logout_member("Manager").getData())
        self.assertTrue(self.user_proxy.logout_member("Manager").isError())
        guestId = self.user_proxy.login_guest().getData().getUserID()
        self.assertTrue(self.user_proxy.login_member(guestId, "Manager", "1234").getData())
        self.user_proxy.exit_system(guestId)

    def test_logout_login_logout(self):
        self.user_proxy.login_member(self.__guestId1, "user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1").getData())

        self.__guestId2 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.__guestId2, "user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1").getData())
        self.user_proxy.exit_system(self.__guestId2)

    def test_logout_FAIL(self):
        user_id = self.user_proxy.login_member(self.__guestId1, "user1", "1234").getData().getUserID()

        self.assertTrue(self.user_proxy.logout_member("no user").isError())

        self.user_proxy.logout_member(user_id)
        self.assertTrue(self.user_proxy.logout_member(user_id).isError())

    def test_logout_twice(self):
        self.user_proxy.login_member(self.__guestId1, "user1", "1234")
        self.assertTrue(self.user_proxy.logout_member("user1").getData())
        self.assertTrue(self.user_proxy.logout_member("user1").isError())

    def test_threaded_logout_twice(self):
        self.user_proxy.login_member(self.__guestId1, "user1", "1234")
        t1 = ThreadWithReturn(target=self.user_proxy.logout_member, args=(("user1"),))
        t2 = ThreadWithReturn(target=self.user_proxy.logout_member, args=(("user1"),))
        t1.start()
        t2.start()
        ans1 = t1.join()
        ans2 = t2.join()
        print(ans1)
        print(ans2)
        self.assertTrue(ans1.isError() or ans2.isError())
        self.assertTrue(ans1.getData() is True or ans2.getData() is True)



if __name__ == '__main__':
    unittest.main()
