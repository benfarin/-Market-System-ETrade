import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Service.MemberService import MemberService
from Service.UserService import UserService


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.user_proxy = UserProxyBridge(UserRealBridge())
        self.market_proxy = MarketProxyBridge(MarketRealBridge())
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)

        self.__guestId = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register(self.__guestId, "user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, "HaPoalim")
        self.founder = self.user_proxy.login_member("user1", "1234").getData().getUserID()

    def test_removeStore(self):
        storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                             0, "000000").getData().getStoreId()
        self.assertTrue(self.user_proxy.removeStore(storeId, self.founder).getData())

    def test_removeStore_Fail(self):
        self.assertTrue(self.user_proxy.removeStore(10, self.founder).isError())
        storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                             0, "000000").getData().getStoreId()
        self.assertTrue(self.user_proxy.removeStore(storeId, 10).isError())

    def test_recreate_store(self):
        storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                             0, "000000").getData().getStoreId()
        self.user_proxy.removeStore(storeId, self.founder)
        self.assertTrue(self.user_proxy.recreateStore(self.founder, storeId).getData())

    def test_recreateStore_Fail(self):
        self.assertTrue(self.user_proxy.recreateStore(10, self.founder).isError())

        storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                             0, "000000").getData().getStoreId()
        self.assertTrue(self.user_proxy.recreateStore(storeId, self.founder).isError())

        self.user_proxy.removeStore(storeId, self.founder)
        self.assertTrue(self.user_proxy.recreateStore(storeId, 10).isError())



if __name__ == '__main__':
    unittest.main()
