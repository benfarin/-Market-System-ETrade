import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseAppointStoreManager(unittest.TestCase):
    # use-case 4.6

    def setUp(self):
        self.proxy_market = MarketProxyBridge(MarketRealBridge())
        self.proxy_user = UserProxyBridge(UserRealBridge())

        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)

        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser", "1234", "0540000000", 123, 1,"Israel", "Beer Sheva", "Rager", 1, 0)
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "4321", "0540000001", 124, 1, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "4321", "0540000002", 124, 1, "Israel", "Beer Sheva",
                                "Rager", 1, 0)
        self.__guestId4 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser4", "4321", "0540000003", 124, 1, "Israel", "Tel aviv",
                                "Rager", 1, 0)

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.user1_id = self.proxy_user.login_member(self.__guestId1, "testUser", "1234").getData().getUserID()
        self.user2_id = self.proxy_user.login_member(self.__guestId2, "testUser2", "4321").getData().getUserID()
        self.user3_id = self.proxy_user.login_member(self.__guestId3, "testUser3", "4321").getData().getUserID()
        self.user4_id = self.proxy_user.login_member(self.__guestId4, "testUser4", "4321").getData().getUserID()
        self.store_id = self.proxy_user.open_store("testStore", self.user1_id, 123, 1, "Israel", "Beer Sheva", "Rager",
                                                 1, 00000).getData().getStoreId()

    def test_AppointStoreManagerPositive(self):
        # store_id, assigner_id, assignee_id
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser2").getData())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser3").getData())

    def test_AppointStoreManagerNoStore(self):
        self.assertTrue(self.proxy_market.appoint_store_manager(-1, self.user1_id,  "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(-2, self.user1_id,  "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(-3, self.user1_id,  "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(-4, self.user1_id,  "testUser2").isError())

    def test_AppointStoreManagerNoOwner(self):
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, -1,  "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, -2,  "testUser3").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, -3,  "testUser4").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, -4,  "testUser2").isError())

    def test_AppointStoreManagerNoNewManager(self):
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "noUser1").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "2543").isError())

    def test_AppointStoreManagerTwice(self):
        # user was already appointed
        self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser2")
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id,  "testUser2").isError())
        self.proxy_user.logout_member(self.user1_id)
        self.proxy_user.login_member(self.user1_id, "testUser", "1234")
        self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser3")
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user1_id, "testUser3").isError())

    def test_AppointStoreManagerNoPermission(self):
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user2_id, "testUser3").isError())
        self.assertTrue(self.proxy_market.appoint_store_manager(self.store_id, self.user2_id, "testUser4").isError())


if __name__ == '__main__':
    unittest.main()
