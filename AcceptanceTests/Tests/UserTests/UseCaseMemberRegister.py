import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UseCaseMemberRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proxy = UserProxyBridge(UserRealBridge())

    def test_register_positive(self):
        try:
            self.__guestId = self.proxy.login_guest().getData().getUserID()
            self.proxy.register(self.__guestId, "user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_register_negative(self):
        self.__guestId1 = self.proxy.login_guest().getData().getUserID()
        self.__guestId2 = self.proxy.login_guest().getData().getUserID()

        t1 = ThreadWithReturn(target=self.proxy.register, args=(self.__guestId1, "user2", "1234", "0500000000", "500",
                                                                "20", "Israel", "Beer Sheva", "Ben Gurion", 0, "HaPoalim"))
        t2 = ThreadWithReturn(target=self.proxy.register, args=(self.__guestId2, "user2", "123456", "0505555555", "501",
                                                                "200", "UK", "Tel Aviv", "center", 1, "Leomit"))
        try:
            t1.start()
            t2.start()
            self.assertTrue(False)
        except:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
