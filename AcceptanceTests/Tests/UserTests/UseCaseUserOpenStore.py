import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService


class UseCaseUserOpenStore(unittest.TestCase):

    #usecase 3.2
    user_proxy = UserProxyBridge(UserRealBridge())
    market_proxy = MarketProxyBridge(MarketRealBridge())

    def setUp(self):
        # assign system manager
        self.user_proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(admin_id, "manager", "1234")

        self.__guestId1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.founder1_id = self.user_proxy.login_member(self.__guestId1, "user1", "1234").getData().getUserID()

        self.__guestId2 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user2", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.founder2_id = self.user_proxy.login_member(self.__guestId2, "user2", "1234").getData().getUserID()

        self.__guestId3 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user3", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.founder3_id = self.user_proxy.login_member(self.__guestId3, "user3", "1234").getData().getUserID()

    def tearDown(self) -> None:
        self.user_proxy.removeMember("manager", "user1")
        self.user_proxy.removeMember("manager", "user2")
        self.user_proxy.removeMember("manager", "user3")
        self.user_proxy.removeSystemManger_forTests("manager")

    def test_open_store_positive1(self):
        store = self.user_proxy.open_store("store-1", self.founder1_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                           0, "000000")
        self.assertEqual(store.getData().getStoreId(), 0)
        print(store.__str__())

    def test_open_stores_in_the_same_time(self):
        store = self.user_proxy.open_store("store-1", self.founder1_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                           0, "000000")

        t1 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-1", self.founder1_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000"))
        t2 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-2", self.founder2_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000"))
        t3 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-3", self.founder2_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000"))
        t4 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-4", self.founder3_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000"))
        t5 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-5", self.founder3_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000"))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        sIds = [t1.join().getData().getStoreId(), t2.join().getData().getStoreId(), t3.join().getData().getStoreId(),
                t4.join().getData().getStoreId(), t5.join().getData().getStoreId()]

        for i in range(5):
            sd_i = sIds[i]
            for j in range(5):
                if i != j:
                    self.assertNotEqual(sd_i, sIds[j])
            print("id of store " + str(i + 1) + " is: " + str(sIds[i]))

    def test_open_store_Fail(self):
        self.assertTrue(self.user_proxy.open_store("store-1", 100, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").isError())

        guestId = self.user_proxy.login_guest().getData().getUserID()
        self.assertTrue(self.user_proxy.open_store("store-1", guestId, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").isError())

        self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, "HaPoalim")
        guestId = self.user_proxy.login_guest().getData().getUserID()
        self.assertTrue(self.user_proxy.open_store("store-1", guestId, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").isError())


if __name__ == '__main__':
    unittest.main()
