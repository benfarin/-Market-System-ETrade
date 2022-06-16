import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
import logging


class UseCaseGuestLogin(unittest.TestCase):
    # console = logging.StreamHandler()
    # console.setLevel(logging.INFO)
    # # add the handler to the root logger
    # logging.getLogger('').addHandler(console)
    # use-case 2.2
    proxy = UserProxyBridge(UserRealBridge())
    logging.getLogger().setLevel(logging.INFO)

    def setUp(self):
        # assign system manager
        self.proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.admin = self.proxy.login_guest().getData().getUserID()
        self.proxy.login_member(self.admin, "Manager", "1234")

    def tearDown(self):
        self.proxy.removeSystemManger_forTests("Manager")
        self.proxy.reset_management()

    def test_login_simple(self):
        guest = self.proxy.login_guest().getData().getUserID()
        self.assertIsNotNone(guest)
        self.proxy.exit_system(guest)

    def test_massive_login(self):

        t1 = ThreadWithReturn(target=self.proxy.login_guest)
        t2 = ThreadWithReturn(target=self.proxy.login_guest)
        t3 = ThreadWithReturn(target=self.proxy.login_guest)
        t4 = ThreadWithReturn(target=self.proxy.login_guest)
        t5 = ThreadWithReturn(target=self.proxy.login_guest)
        t6 = ThreadWithReturn(target=self.proxy.login_guest)
        t7 = ThreadWithReturn(target=self.proxy.login_guest)
        t8 = ThreadWithReturn(target=self.proxy.login_guest)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()

        uIds = [t1.join().getData().getUserID(), t2.join().getData().getUserID(), t3.join().getData().getUserID(),
                t4.join().getData().getUserID(), t5.join().getData().getUserID(), t6.join().getData().getUserID(),
                t7.join().getData().getUserID(), t8.join().getData().getUserID()]

        for i in range(8):
            Id_i = uIds[i]
            for j in range(8):
                if i != j:
                    self.assertNotEqual(Id_i, uIds[j])
        for id in uIds:
            self.proxy.exit_system(id)



if __name__ == '__main__':
    unittest.main()
