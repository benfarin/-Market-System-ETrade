import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService


class RemoveAndRecreateStore(unittest.TestCase):
    databases = {'testing'}
    user_proxy = UserProxyBridge(UserRealBridge())
    market_proxy = MarketProxyBridge(MarketRealBridge())

    def setUp(self):
        # assign system manager
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "Manager", "1234")

        # create user
        self.__guestId = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("Kfir", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.founder = self.user_proxy.login_member(self.__guestId, "Kfir", "1234").getData().getUserID()
        self.storeId = self.user_proxy.open_store("store", self.founder, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion", 0, "000000").getData().getStoreId()

    def tearDown(self):
        self.market_proxy.removeStoreForGood(self.founder, self.storeId)
        self.user_proxy.removeMember("Manager", "Kfir")
        self.user_proxy.removeSystemManger_forTests("Manager")

    def test_removeStore(self):
        self.assertTrue(self.user_proxy.removeStore(self.storeId, self.founder))


    def test_removeStore_negative(self):
        # store doesn't exist
        self.assertTrue(self.user_proxy.removeStore(-1, self.founder).isError())
        # founder doesn't exist
        self.assertTrue(self.user_proxy.removeStore(self.storeId, -1).isError())
        # remove store twice
        self.assertTrue(self.user_proxy.removeStore(self.storeId, self.founder))
        self.assertTrue(self.user_proxy.removeStore(self.storeId, self.founder).isError())

    def test_recreate_store(self):
        # remove store
        self.user_proxy.removeStore(self.storeId, self.founder)
        # recreate store
        self.assertTrue(self.user_proxy.recreateStore(self.founder, self.storeId).getData())
        # add product to store - should succeed!
        self.assertTrue(self.market_proxy.add_product_to_store(self.storeId, self.founder, "the best product", 100,
                                                                "Category", 8,
                                                                ["Test1", "Test2"]).getData())

    def test_recreateStore_few_cases(self):
        # recreate store that doesn't exist
        self.assertTrue(self.user_proxy.recreateStore(-1, self.founder).isError())
        # recreate store that is open
        self.assertTrue(self.user_proxy.recreateStore(self.storeId, self.founder).isError())
        # remove the store
        self.user_proxy.removeStore(self.storeId, self.founder)
        # recreate that store
        self.assertFalse(self.user_proxy.recreateStore(self.founder, self.storeId).isError())


if __name__ == '__main__':
    unittest.main()
