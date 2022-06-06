import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UseCaseMemberRegister(unittest.TestCase):
    # usecase 2.3
    proxy = UserProxyBridge(UserRealBridge())

    def setUp(self):
        self.proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1).getData()
        admin_id = self.proxy.login_guest().getData().getUserID()
        self.proxy.login_member(admin_id, "manager", "1234")
        self.__guestId_0 = self.proxy.login_guest().getData().getUserID()
        # self.systemManger = self.proxy.login_member(self.__guestId_0, "manager", "1234").getData()

    def tearDown(self):
        self.proxy.exit_system(self.__guestId_0)
        self.proxy.removeSystemManger_forTests("manager")

    def test_register_positive_one(self):
        guestId = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 0)
        self.assertTrue(self.proxy.login_member(guestId, "user1", "1234").getData())

        # remove the user
        self.proxy.removeMember("manager", "user1")

    def test_register_positive_two(self):
        guestId1 = self.proxy.login_guest().getData().getUserID()
        guestId2 = self.proxy.login_guest().getData().getUserID()

        t1 = ThreadWithReturn(target=self.proxy.register, args=("user1", "1234", "0500000000", "500",
                                                                "20", "Israel", "Beer Sheva", "Ben Gurion", 0, 0))
        t2 = ThreadWithReturn(target=self.proxy.register, args=("user2", "123456", "0505555555", "501",
                                                                "200", "UK", "Tel Aviv", "center", 1, 0))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.assertTrue(
            self.proxy.login_member(guestId1, "user1", "1234").getData() and self.proxy.login_member(guestId2, "user2",
                                                                                                     "123456").getData())
        # tear down stuff
        self.proxy.removeMember("manager", "user1")
        self.proxy.removeMember("manager", "user2")

    def test_register_negative_same_username(self):
        guestId1 = self.proxy.login_guest().getData().getUserID()
        guestId2 = self.proxy.login_guest().getData().getUserID()

        t1 = ThreadWithReturn(target=self.proxy.register, args=("user1", "1234", "0500000000", "500",
                                                                "20", "Israel", "Beer Sheva", "Ben Gurion", 0, 0))
        t2 = ThreadWithReturn(target=self.proxy.register, args=("user1", "123456", "0505555555", "501",
                                                                "200", "UK", "Tel Aviv", "center", 1, 0))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.assertFalse(
            self.proxy.login_member(guestId1, "user1", "1234").getData() and self.proxy.login_member(guestId2, "user2",
                                                                                                     "123456").getData())

        # tear down stuff
        self.proxy.removeMember("manager", "user1")
        self.proxy.removeMember("manager", "user2")

    def test_register_positive_same_username(self):
        guestId1 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 0)
        self.proxy.login_member(guestId1, "user1", "1234").getData().getUserID()

        self.assertTrue(self.proxy.register("user1", "12345", "0500000001", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 0).isError())

        self.proxy.removeMember("manager", "user1")
        guestId2 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user1", "12345", "0500000001", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 0)
        self.assertTrue(self.proxy.login_member(guestId2, "user1", "12345").getData())

        # teardown stuff
        self.proxy.removeMember("manager", "user1")


if __name__ == '__main__':
    unittest.main()
