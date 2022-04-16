import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class UseCaseMemberRegister(unittest.TestCase):
    def setUp(self):
        self.proxy = UserProxyBridge(None)

    def test_register_positive(self):
        self.assertEqual(self.proxy.register("TestUser", "TestPassword", "TestPassword", "TestEmail"), True)

    def test_register_negative(self):
        self.proxy.register("TestUser", "TestPassword", "TestPassword", "TestEmail")
        self.assertEqual(self.proxy.register("TestUser", "TestPassword2", "TestPassword2", "TestEmail2"), False)

    def test_register_negative2(self):
        self.proxy.register("TestUser", "TestPassword", "TestPassword", "TestEmail")
        self.assertEqual(self.proxy.register("TestUser2", "TestPassword2", "TestPassword2", "TestEmail"), False)

    def test_register_negative3(self):
        self.proxy.register("TestUser", "TestPassword", "TestPassword", "TestEmail")
        self.assertEqual(self.proxy.register("TestUser2", "TestPassword", "TestPassword2", "TestEmail2"), False)


if __name__ == '__main__':
    unittest.main()
