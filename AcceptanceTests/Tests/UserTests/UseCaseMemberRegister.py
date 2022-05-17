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
        self.__guestId = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                         "Ben Gurion", 0, "HaPoalim")
        self.assertEqual(self.proxy.login_member(self.__guestId, "user1", "1234").getData().getPhone(), "0500000000")


if __name__ == '__main__':
    unittest.main()
