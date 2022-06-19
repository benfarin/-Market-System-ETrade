import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UseCaseMemberRegister(unittest.TestCase):
    # usecase 2.3
    databases = {'testing'}
    proxy = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign system manager
        self.proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1).getData()
        self.admin_id = self.proxy.login_guest().getData().getUserID()
        self.proxy.login_member(self.admin_id, "manager", "1234")

    def tearDown(self):
        self.proxy.removeMember("manager", "user1")
        self.proxy.removeMember("manager", "user2")
        self.proxy.removeSystemManger_forTests("manager")
        self.proxy.reset_management()

    def test_register_positive_one(self):
        self.assertTrue(self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 0))

    def test_register_positive_two(self):
        t1 = ThreadWithReturn(target=self.proxy.register, args=("user1", "1234", "0500000000", "500",
                                                                "20", "Israel", "Beer Sheva", "Ben Gurion", 0, 0))
        t2 = ThreadWithReturn(target=self.proxy.register, args=("user2", "123456", "0505555555", "501",
                                                                "200", "UK", "Tel Aviv", "center", 1, 0))
        t1.start()
        t2.start()
        self.assertTrue(t1.join() and t2.join())

    def test_register_negative_same_username(self):
        t1 = ThreadWithReturn(target=self.proxy.register, args=("user1", "1234", "0500000000", "500",
                                                                "20", "Israel", "Beer Sheva", "Ben Gurion", 0, 0))
        t2 = ThreadWithReturn(target=self.proxy.register, args=("user1", "123456", "0505555555", "501",
                                                                "200", "UK", "Tel Aviv", "center", 1, 0))
        t1.start()
        t2.start()
        ans1 = t1.join()
        ans2 = t2.join()
        self.assertTrue(ans1.isError() or ans2.isError())

    def test_register_same_username(self):
        self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 0)

        self.assertTrue(self.proxy.register("user1", "12345", "0500000001", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 0).isError())

        self.proxy.removeMember("manager", "user1")
        self.assertTrue(self.proxy.register("user1", "12345", "0500000001", "500", "20", "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 0))



if __name__ == '__main__':
    unittest.main()
