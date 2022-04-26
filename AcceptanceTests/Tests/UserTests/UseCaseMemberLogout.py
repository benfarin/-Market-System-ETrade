import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge


class UseCaseMemberLogout(unittest.TestCase):
    def setUp(self):
        self.user_proxy = UserProxyBridge(None)
        self.user_id = self.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                                "Ben Gurion", 0, "HaPoalim", None)

    def test_logout_positive1(self):
        self.user_proxy.login_member(self.user_id, "1234")
        self.assertEqual(self.user_proxy.logout_member(self.user_id), True)

    def test_logout_negative1(self):
        self.assertEqual(self.user_proxy.logout("User1"), False)

    def test_logout_negative2(self):
        self.user_proxy.login_member(self.user_id, "1234")
        self.assertEqual(self.user_proxy.logout(-999), False)


if __name__ == '__main__':
    unittest.main()
