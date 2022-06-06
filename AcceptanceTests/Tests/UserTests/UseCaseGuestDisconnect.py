import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseGuestDisconnect(unittest.TestCase):
    #usecase 2.2
    proxy = UserProxyBridge(UserRealBridge())

    def setUp(self) -> None:
        # assign system manager
        self.proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        admin_id = self.proxy.login_guest().getData().getUserID()
        self.proxy.login_member(admin_id, "manager", "1234")

    def tearDown(self) -> None:
        self.proxy.removeSystemManger_forTests("manager")

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
