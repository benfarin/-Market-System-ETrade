import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.user_proxy = UserProxyBridge(None)
        self.user_proxy.register("User1", "Password", "Password", "Email")

    def test_logout_positive1(self):
        self.user_proxy.login("User1", "Password")
        self.assertEqual(self.user_proxy.logout("User1"), True)

    def test_logout_negative1(self):
        self.user_proxy.login("User1", "Password")
        self.assertEqual(self.user_proxy.logout("User2"), False)

    def test_logout_negative2(self):
        self.assertEqual(self.user_proxy.logout("User1"), False)


if __name__ == '__main__':
    unittest.main()
