import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UseCaseMemberRegister(unittest.TestCase):
    #usecase 2.3


    def setUp(self):
        self.proxy = UserProxyBridge(UserRealBridge())

    def test_register_positive_one(self):
        guestId = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                         "Ben Gurion", 0, "HaPoalim")
        self.assertTrue(self.proxy.login_member(guestId, "user1", "1234").getData())

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
        self.assertTrue(self.proxy.login_member(guestId1, "user1", "1234").getData() and self.proxy.login_member(guestId2, "user2", "123456").getData())

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
        self.assertFalse(self.proxy.login_member(guestId1, "user1", "1234").getData() and self.proxy.login_member(guestId2, "user2",
                                                                                                     "123456").getData())

    def test_register_positive_same_username(self):
        guestId1 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                         "Ben Gurion", 0, "HaPoalim")
        user1 = self.proxy.login_member(guestId1, "user1", "1234").getData().getUserID()
        self.proxy.logout_member(user1)
        self.proxy.exit_system(guestId1)

        guestId2 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user1", "12345", "0500000001", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, "HaPoalim")
        self.assertTrue(self.proxy.login_member(guestId2, "user1", "12345").getData())
        # should be ok because user1 exited the system -> his username is available





if __name__ == '__main__':
    unittest.main()
