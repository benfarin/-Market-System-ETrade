import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseSystemInitialization(unittest.TestCase):
    #usecase 1.1
    # check there is always a system manager in the system

    def setUp(self) -> None:
        self.proxy = UserProxyBridge(UserRealBridge())

    # def test_Positive(self):
    #     system_manager = self.proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
    #                                       "Ben Gurion", 1, 1).getData().getUserID()
    #     self.proxy.exit_system(system_manager)

    # def test_systemManagerExitsSystem(self):
    #     system_manager = self.proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
    #                                       "Ben Gurion", 1, 1)



if __name__ == '__main__':
    unittest.main()
