import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Service.MemberService import MemberService
from Service.UserService import UserService


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.proxy = UserProxyBridge(UserRealBridge())
        self.proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)

    def test_login(self):
        try:
            self.proxy.login_guest()
            self.assertTrue(True)
        except:
            self.assertTrue(False)


    def test_massive_login(self):

        t1 = ThreadWithReturn(target=self.proxy.login_guest)
        t2 = ThreadWithReturn(target=self.proxy.login_guest)
        t3 = ThreadWithReturn(target=self.proxy.login_guest)

        t1.start()
        t2.start()
        t3.start()

        print(t1.join().getData().getUserID())
        print(t2.join().getData().getUserID())
        print(t3.join().getData().getUserID())



if __name__ == '__main__':
    unittest.main()
