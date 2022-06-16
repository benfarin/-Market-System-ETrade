import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseGuestDisconnect(unittest.TestCase):
    # use-case 2.2
    proxy = UserProxyBridge(UserRealBridge())

    def setUp(self) -> None:
        # assign system manager
        self.proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.proxy.login_guest().getData().getUserID()
        self.proxy.login_member(self.admin_id, "manager", "1234")

    def tearDown(self):
        self.proxy.exit_system(self.admin_id)
        self.proxy.removeSystemManger_forTests("manager")
        self.proxy.reset_management()

    def test_positive(self):
        guest_id = self.__guestId1 = self.proxy.login_guest().getData().getUserID()
        self.assertTrue(self.proxy.exit_system(guest_id))


    def test_negative(self):
        # guest can't exit twice
        guest_id = self.proxy.login_guest().getData().getUserID()
        self.proxy.exit_system(guest_id)
        res = self.proxy.exit_system(guest_id).getError()
        string = "The member " + str(guest_id) + " not online!"
        self.assertEqual(str(res), string, "guest was able to exit before logging in")


if __name__ == '__main__':
    unittest.main()
