import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UseCaseMemberLogin(unittest.TestCase):
    #usecase 2.4
    proxy = UserProxyBridge(UserRealBridge())

    def setUp(self):
        self.proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                         "Ben Gurion", 1, 1)
        self.admin = self.proxy.login_guest().getData().getUserID()
        self.proxy.login_member(self.admin, "Manager", "1234")
        self.__guestId1 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                           "Ben Gurion", 0, 1)

    def tearDown(self):
        self.proxy.exit_system(self.admin)
        self.proxy.exit_system(self.__guestId1)
        self.proxy.removeMember("Manager", "user1")
        self.proxy.removeSystemManger_forTests("Manager")
        self.proxy.reset_management()

    def test_login_positive(self):
        member = self.proxy.login_member(self.__guestId1, "user1", "1234")
        self.assertTrue(member.getData())
        print(member.__str__())

    def test_members_log_in_together(self):
        self.__guestId2 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 1)
        self.__guestId3 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user3", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 1)
        self.__guestId4 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user4", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 1)
        self.__guestId5 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register( "user5", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 1)
        self.__guestId6 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user6", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 1)
        self.__guestId7 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user7", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 1)

        t2 = ThreadWithReturn(target=self.proxy.login_member, args=(self.__guestId2, "user2", "1234"))
        t3 = ThreadWithReturn(target=self.proxy.login_member, args=(self.__guestId3, "user3", "1234"))
        t4 = ThreadWithReturn(target=self.proxy.login_member, args=(self.__guestId4, "user4", "1234"))
        t5 = ThreadWithReturn(target=self.proxy.login_member, args=(self.__guestId5, "user5", "1234"))
        t6 = ThreadWithReturn(target=self.proxy.login_member, args=(self.__guestId6, "user6", "1234"))
        t7 = ThreadWithReturn(target=self.proxy.login_member, args=(self.__guestId7, "user7", "1234"))

        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()

        uIds = [t2.join().getData().getUserID(), t3.join().getData().getUserID(), t4.join().getData().getUserID(),
                t5.join().getData().getUserID(), t6.join().getData().getUserID(), t7.join().getData().getUserID()]

        for i in range(6):
            Id_i = uIds[i]
            for j in range(6):
                if i != j:
                    self.assertNotEqual(Id_i, uIds[j])
            print("id of user " + str(i + 2) + " is: " + str(uIds[i]))

        self.proxy.exit_system(self.__guestId2)
        self.proxy.exit_system(self.__guestId3)
        self.proxy.exit_system(self.__guestId4)
        self.proxy.exit_system(self.__guestId5)
        self.proxy.exit_system(self.__guestId6)
        self.proxy.exit_system(self.__guestId7)
        self.proxy.removeMember("Manager", "user2")
        self.proxy.removeMember("Manager", "user3")
        self.proxy.removeMember("Manager", "user4")
        self.proxy.removeMember("Manager", "user5")
        self.proxy.removeMember("Manager", "user6")
        self.proxy.removeMember("Manager", "user7")


    def test_login_twice(self):
        guest2 = self.proxy.login_guest().getData().getUserID()
        self.proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                            "Ben Gurion", 0, 1)
        self.assertTrue(self.proxy.login_member(guest2, "user2", "1234").getData())
        self.assertTrue(self.proxy.login_member(guest2, "user2", "1234").isError())


        self.proxy.exit_system(guest2)
        self.proxy.removeMember("Manager", "user2")

    # def test_threaded_login_twice(self):
    #     guest2 = self.proxy.login_guest().getData().getUserID()
    #     self.proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
    #                         "Ben Gurion", 0, 1)
    #     t1 = ThreadWithReturn(target=self.proxy.login_member, args=(guest2, "user2", "1234"))
    #     t2 = ThreadWithReturn(target=self.proxy.login_member, args=(guest2, "user2", "1234"))
    #
    #     t1.start()
    #     t2.start()
    #
    #     ans1 = t1.join()
    #     ans2 = t2.join()
    #     self.assertTrue(ans1.isError() or ans2.isError())
    #     self.assertTrue(ans1.getData() is True or ans2.getData() is True)
    #
    #     self.proxy.removeMember("Manager", "user2")

if __name__ == '__main__':
    unittest.main()
