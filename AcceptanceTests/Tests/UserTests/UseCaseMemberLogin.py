import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class UseCaseMemberLogin(unittest.TestCase):
    def setUp(self):
        self.proxy = UserProxyBridge(None)

    def test_login_positive(self):
        id = self.proxy.register("UserNameTest", "PasswordTest", "EmailTest")
        self.assertEqual(self.proxy.login(id, "PasswordTest"), True)

    def test_login_negative(self):
        self.assertEqual(self.proxy.login(-999, "PasswordTest"), False)


if __name__ == '__main__':
    unittest.main()
