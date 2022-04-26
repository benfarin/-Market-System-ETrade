import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class UseCaseMemberLogin(unittest.TestCase):
    def setUp(self):
        self.proxy = UserProxyBridge(None)
        self.id = self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva", "Ben Gurion", 0, "HaPoalim", None)

    def test_login_positive(self):
        self.assertEqual(self.proxy.login_member(self.id, "1234"), True)

    def test_login_negative1(self):
        self.assertEqual(self.proxy.login(-999, "PasswordTest"), False)

    def test_login_negative2(self):
        self.assertEqual(self.proxy.login(self.id, "PasswordTest"), False)

    def test_login_negative3(self):
        self.proxy.login_member(self.id, "1234")
        self.assertEqual(self.proxy.login(self.id, "1234"), False)


if __name__ == '__main__':
    unittest.main()
