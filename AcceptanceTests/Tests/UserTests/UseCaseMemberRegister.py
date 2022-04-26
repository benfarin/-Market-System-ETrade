import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MarketService import MarketService
from Service.UserService import UserService


class UseCaseMemberRegister(unittest.TestCase):
    def setUp(self):
        self.proxy = UserProxyBridge(UserRealBridge(UserService(), MarketService()))

    def test_register_positive(self):
        self.assertEqual(self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim", None), True)

    def test_register_negative(self):
        self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva", "Ben Gurion", 0,
                            "HaPoalim", None)
        self.assertEqual(self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim", None), False)

    def test_register_negative2(self):
        self.assertEqual(self.proxy.register("user2", "", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim", None), False)


if __name__ == '__main__':
    unittest.main()
