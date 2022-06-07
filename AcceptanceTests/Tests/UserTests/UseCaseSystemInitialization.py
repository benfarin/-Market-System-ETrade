import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseSystemInitialization(unittest.TestCase):
    #usecase 1.1
    # check there is always a system manager in the system
    proxy = UserProxyBridge(UserRealBridge())

    def test_remove_system_manager(self):
        # assign system manager
        self.proxy.appoint_system_manager("Rotem", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        admin_id = self.proxy.login_guest().getData().getUserID()
        self.proxy.login_member(admin_id, "Rotem", "1234")
        # login should succeed
        self.assertTrue(self.proxy.login_guest().getData())
        # system manager exits system
        self.proxy.removeSystemManger_forTests("Rotem")
        # login should fail - no system manager
        self.assertFalse(self.proxy.login_guest().getData())


if __name__ == '__main__':
    unittest.main()
