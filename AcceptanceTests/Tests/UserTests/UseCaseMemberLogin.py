import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.proxy = UserProxyBridge(None)

    def test_login_positive(self):
        self.proxy.register("UserNameTest", "PasswordTest", "EmailTest")
        self.assertEqual(self.proxy.login("UserNameTest", "PasswordTest"), True)

    def test_login_negative(self):
        self.assertEqual(self.proxy.login("UserName2Test", "PasswordTest"), False)


if __name__ == '__main__':
    unittest.main()
