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
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "manager", "1234")

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
        self.user_proxy.exit_system(self.admin_id)
        self.user_proxy.exit_system(self.__guestId1)
        self.user_proxy.exit_system(self.__guestId2)
        self.user_proxy.exit_system(self.__guestId3)
        self.user_proxy.removeMember("manager", "user1")
        self.user_proxy.removeMember("manager", "user2")
        self.user_proxy.removeMember("manager", "user3")
        self.user_proxy.removeSystemManger_forTests("manager")

    def test_open_store_positive1(self):
        store = self.user_proxy.open_store("store-1", self.founder1_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                           0, "000000")
        self.assertTrue(store.getData())

        self.market_proxy.removeStoreForGood(self.founder1_id, store.getData().getStoreId())

    def test_open_stores_at_the_same_time(self):
        t1 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-1", self.founder1_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000",))
        t2 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-2", self.founder2_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000",))
        t3 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-3", self.founder2_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000",))
        t4 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-4", self.founder3_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000",))
        t5 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-5", self.founder3_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000",))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        sIds = [t1.join().getData().getStoreId(), t2.join().getData().getStoreId(), t3.join().getData().getStoreId(),
                t4.join().getData().getStoreId(), t5.join().getData().getStoreId()]

        for i in range(4):
            sd_i = sIds[i]
            for j in range(4):
                if i != j:
                    self.assertNotEqual(sd_i, sIds[j])
            print("id of store " + str(i + 1) + " is: " + str(sIds[i]))

        self.market_proxy.removeStoreForGood(self.founder1_id, sIds[0])
        self.market_proxy.removeStoreForGood(self.founder2_id, sIds[1])
        self.market_proxy.removeStoreForGood(self.founder2_id, sIds[2])
        self.market_proxy.removeStoreForGood(self.founder3_id, sIds[3])
        self.market_proxy.removeStoreForGood(self.founder3_id, sIds[4])



    def test_open_store_few_cases(self):
        # founder doesn't exit
        self.assertTrue(self.user_proxy.open_store("store-1", -1, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").isError())

        # guest can't open a store
        guestId = self.user_proxy.login_guest().getData().getUserID()
        self.assertTrue(self.user_proxy.open_store("store-1", guestId, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").isError())

        self.user_proxy.register("user4", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        founder = self.user_proxy.login_member(guestId, "user4", "1234").getData().getUserID()
        store = self.user_proxy.open_store("store-1", founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                           0, "000000")
        self.assertTrue(store.getData())

        self.market_proxy.removeStoreForGood(founder, store.getData().getStoreId())
        self.user_proxy.removeMember("manager", "user4")
        self.user_proxy.exit_system(guestId)




if __name__ == '__main__':
    unittest.main()
