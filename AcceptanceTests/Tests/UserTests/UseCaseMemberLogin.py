import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UseCaseMemberLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proxy = UserProxyBridge(UserRealBridge())
        cls.proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                         "Ben Gurion", 1, 1)
        cls.__guestId1 = cls.proxy.login_guest().getData().getUserID()
        cls.proxy.register(cls.__guestId1, "user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                           "Ben Gurion", 0, 1)

    def test_login_positive(self):
        member = self.proxy.login_member("user1", "1234")
        self.assertTrue(member.getData())
        print(member.__str__())

    def test_login_negative1(self):
        self.assertRaises(Exception, self.proxy.login_member("user2", "PasswordTest"))

    def test_login_negative2(self):
        self.assertRaises(Exception, self.proxy.login_member("user1", "PasswordTest"))

    def test_massive_login(self):
        t1 = ThreadWithReturn(target=self.proxy.login_guest)
        t2 = ThreadWithReturn(target=self.proxy.login_guest)
        t3 = ThreadWithReturn(target=self.proxy.login_guest)

        t1.start()
        t2.start()
        t3.start()

        print(t1.join().getData().getUserID())
        print(t2.join().getData().getUserID())
        print(t3.join().getData().getUserID())


if __name__ == '__main__':
    unittest.main()
