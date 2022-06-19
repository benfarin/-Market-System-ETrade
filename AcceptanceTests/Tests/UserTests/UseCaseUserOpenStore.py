import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService


class UseCaseUserOpenStore(unittest.TestCase):
    # usecase 3.2
    databases = {'testing'}
    user_proxy = UserProxyBridge(UserRealBridge())
    market_proxy = MarketProxyBridge(MarketRealBridge())

    def setUp(self):
        # assign system manager
        self.user_proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "manager", "1234")

        self.__guestId1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("Niv", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.founder1_id = self.user_proxy.login_member(self.__guestId1, "Niv", "1234").getData().getUserID()

        self.__guestId2 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("Bar", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.founder2_id = self.user_proxy.login_member(self.__guestId2, "Bar", "1234").getData().getUserID()

        self.__guestId3 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("Ori", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.founder3_id = self.user_proxy.login_member(self.__guestId3, "Ori", "1234").getData().getUserID()
        # initialize variables
        self.sIds = []
        self.store = -1

    def tearDown(self):
        #remove stores
        if self.store != -1:
            self.market_proxy.removeStoreForGood(self.founder1_id, self.store.getData().getStoreId())
        if len(self.sIds) > 0:
            self.market_proxy.removeStoreForGood(self.founder1_id, self.sIds[0])
            self.market_proxy.removeStoreForGood(self.founder2_id, self.sIds[1])
            self.market_proxy.removeStoreForGood(self.founder2_id, self.sIds[2])
        self.user_proxy.removeMember("manager", "Niv")
        self.user_proxy.removeMember("manager", "Ori")
        self.user_proxy.removeMember("manager", "Bar")
        self.user_proxy.removeMember("manager", "Rotem")
        self.user_proxy.removeSystemManger_forTests("manager")

    def test_open_store_positive1(self):
        self.store = self.user_proxy.open_store("Niv's store", self.founder1_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                           0, "000000")
        self.assertTrue(self.store.getData())

    def test_open_stores_at_the_same_time(self):
        t1 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-1", self.founder1_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000",))
        t2 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-2", self.founder2_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000",))
        t3 = ThreadWithReturn(target=self.user_proxy.open_store, args=("store-3", self.founder3_id, 0, 0,
                                                                       "israel", "Beer-Sheva", "Ben-Gurion",
                                                                       0, "000000",))

        t1.start()
        t2.start()
        t3.start()


        self.sIds = [t1.join().getData().getStoreId(), t2.join().getData().getStoreId(), t3.join().getData().getStoreId()]


        for i in range(3):
            sd_i = self.sIds[i]
            for j in range(3):
                if i != j:
                    self.assertNotEqual(sd_i, self.sIds[j])

    def test_open_store_few_cases(self):
        # founder doesn't exit
        self.assertTrue(self.user_proxy.open_store("store-1", -1, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").isError())

        # guest can't open a store
        guestId = self.user_proxy.login_guest().getData().getUserID()
        self.assertTrue(self.user_proxy.open_store("store-1", guestId, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                   0, "000000").isError())

        self.user_proxy.register("Rotem", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        founder = self.user_proxy.login_member(guestId, "Rotem", "1234").getData().getUserID()
        self.store = self.user_proxy.open_store("store-1", founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                           0, "000000")
        self.assertTrue(self.store.getData())

        self.market_proxy.removeStoreForGood(founder, self.store.getData().getStoreId())




if __name__ == '__main__':
    unittest.main()
