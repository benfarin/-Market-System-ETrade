import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.proxy = UserProxyBridge(None)

    def test_login(self):
        self.assertEqual(self.proxy.login_guest(), True)


if __name__ == '__main__':
    unittest.main()
