import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService


class RemoveAndRecreateStore(unittest.TestCase):
    user_proxy = UserProxyBridge(UserRealBridge())
    market_proxy = MarketProxyBridge(MarketRealBridge())

    def setUp(self):
        # assign system manager
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "Manager", "1234")

        self.__guestId = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.founder = self.user_proxy.login_member(self.__guestId, "user1", "1234").getData().getUserID()

    def tearDown(self) -> None:
        self.user_proxy.exit_system(self.admin_id)
        self.user_proxy.exit_system(self.__guestId)
        self.user_proxy.removeMember("Manager", "user1")
        self.user_proxy.removeSystemManger_forTests("Manager")

    def test_removeStore(self):
        storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                             0, "000000").getData().getStoreId()
        self.assertTrue(self.user_proxy.removeStore(storeId, self.founder).getData())

        # remove store!
        self.market_proxy.removeStoreForGood(self.founder, storeId)

    def test_removeStore_negative(self):
        # store doesn't exist
        self.assertTrue(self.user_proxy.removeStore(10, self.founder).isError())
        storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                             0, "000000").getData().getStoreId()
        # founder doesn't exist
        self.assertTrue(self.user_proxy.removeStore(storeId, 10).isError())

        self.market_proxy.removeStoreForGood(self.founder, storeId)


    def test_recreate_store(self):
        storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                             0, "000000").getData().getStoreId()
        self.user_proxy.removeStore(storeId, self.founder)
        self.assertTrue(self.user_proxy.recreateStore(self.founder, storeId).getData())

        # teardown stuff
        self.market_proxy.removeStoreForGood(self.founder, storeId)

    def test_recreateStore_few_cases(self):
        # recreate store that doesn't exist
        self.assertTrue(self.user_proxy.recreateStore(10, self.founder).isError())

        storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                             0, "000000").getData().getStoreId()
        # recreate store that is open
        self.assertTrue(self.user_proxy.recreateStore(storeId, self.founder).isError())

        # should work
        self.user_proxy.removeStore(storeId, self.founder)
        self.assertFalse(self.user_proxy.recreateStore(self.founder, storeId).isError())

        # remove for good :)
        self.market_proxy.removeStoreForGood(self.founder, storeId)


if __name__ == '__main__':
    unittest.main()
