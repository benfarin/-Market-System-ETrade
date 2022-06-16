import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseAppointStoreManager(unittest.TestCase):
    # use-case 4.6

    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):

        # assign system manager
        self.proxy_user.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "manager", "1234")

        # create 3 users
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser", "1234", "0540000000", 123, 1,"Israel", "Beer Sheva", "Rager", 1, 0)
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "4321", "0540000001", 124, 1, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "4321", "0540000002", 124, 1, "Israel", "Beer Sheva",
                                "Rager", 1, 0)

        # login 3 users
        self.user1_id = self.proxy_user.login_member(self.__guestId1, "testUser", "1234").getData().getUserID()
        self.user2_id = self.proxy_user.login_member(self.__guestId2, "testUser2", "4321").getData().getUserID()
        self.user3_id = self.proxy_user.login_member(self.__guestId3, "testUser3", "4321").getData().getUserID()

        # create store
        self.store_id = self.proxy_user.open_store("testStore", self.user1_id, 123, 1, "Israel", "Beer Sheva", "Rager",
                                                 1, 00000).getData().getStoreId()

    def tearDown(self) -> None:
        self.proxy_market.removeStoreForGood(self.user1_id, self.store_id)
        self.proxy_user.removeMember("manager", "testUser")
        self.proxy_user.removeMember("manager", "testUser2")
        self.proxy_user.removeMember("manager", "testUser3")
        self.proxy_user.removeSystemManger_forTests("manager")

    def test_AppointStoreManagerPositive(self):
        # assign user2 and user3 to be store's managers
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser2").getData())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser3").getData())
        store = self.proxy_market.get_store_by_ID(self.store_id).getData()
        # get store's managers
        managers = store.getStoreManagers()
        for i in range(len(managers)):
            managers[i] = managers[i].getUserID()
        # check user2 and user3 are the store's managers
        self.assertTrue(managers == [self.user2_id, self.user3_id] or managers ==[self.user3_id, self.user2_id])

    def test_AppointStoreManagerNegativeArgument(self):
        self.assertTrue(self.proxy_market.appoint_store_manager(-1, self.user1_id,  "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, -1,  "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "noUser1").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "").isError())

    def test_AppointStoreManagerTwice(self):
        # user was already appointed
        self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser2")
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id,  "testUser2").isError(), "user2 is already manager")
        self.proxy_user.logout_member("testUser")
        self.proxy_user.login_member(self.user1_id, "testUser", "1234")
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser3"))
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser3").isError(), "user3 is already manager")
        store = self.proxy_market.get_store_by_ID(self.store_id).getData()
        # get store's managers
        managers = store.getStoreManagers()
        for i in range(len(managers)):
            managers[i] = managers[i].getUserID()
        # check user2 and user3 are the store's managers
        self.assertEqual(managers, [self.user2_id, self.user3_id] or [self.user3_id, self.user2_id])

    def test_AppointStoreManagerNoPermission(self):
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user2_id, "testUser3").isError())


if __name__ == '__main__':
    unittest.main()
