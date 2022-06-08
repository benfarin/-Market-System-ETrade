import unittest
from collections import Counter

from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge



class UseCaseAppointStoreOwner(unittest.TestCase):
    # use-case 4.4

    # initialize proxies
    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin, "Manager", "1234")

        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser", "1234", "0540000000", 123, 0, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "4321", "0540000001", 124, 1, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "4321", "0540000002", 124, 0, "Israel", "Beer Sheva",
                                "Rager", 1, 0)
        self.__guestId4 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser4", "4321", "0540000003", 124, 2, "Israel", "Tel aviv",
                                "Rager", 1, 0)
        self.__guestId5 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser5", "4321", "0540000003", 124, 2, "Israel", "Tel aviv",
                                 "Rager", 1, 0)
        self.__guestId6 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser6", "4321", "0540000003", 124, 2, "Israel", "Tel aviv",
                                 "Rager", 1, 0)


        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.user1_id = self.proxy_user.login_member(self.__guestId1, "testUser", "1234").getData().getUserID()
        self.user2_id = self.proxy_user.login_member(self.__guestId2, "testUser2", "4321").getData().getUserID()
        self.user3_id = self.proxy_user.login_member(self.__guestId3, "testUser3", "4321").getData().getUserID()
        self.user4_id = self.proxy_user.login_member(self.__guestId4, "testUser4", "4321").getData().getUserID()
        self.user5_id = self.proxy_user.login_member(self.__guestId3, "testUser5", "4321").getData().getUserID()
        self.user6_id = self.proxy_user.login_member(self.__guestId4, "testUser6", "4321").getData().getUserID()
        self.store_id = self.proxy_user.open_store("testStore", self.user1_id, 123, 2, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()


    def tearDown(self) -> None:
        self.proxy_user.exit_system(self.admin)
        self.proxy_user.exit_system(self.__guestId1)
        self.proxy_user.exit_system(self.__guestId2)
        self.proxy_user.exit_system(self.__guestId3)
        self.proxy_user.exit_system(self.__guestId4)
        self.proxy_user.exit_system(self.__guestId5)
        self.proxy_user.exit_system(self.__guestId6)

        # remove the store0*
        self.proxy_market.removeStoreForGood(self.user1_id, self.store_id)
        # remove users
        self.proxy_user.removeMember("Manager", "testUser")
        self.proxy_user.removeMember("Manager", "testUser2")
        self.proxy_user.removeMember("Manager", "testUser3")
        self.proxy_user.removeMember("Manager", "testUser4")
        self.proxy_user.removeMember("Manager", "testUser5")
        self.proxy_user.removeMember("Manager", "testUser6")
        # remove system manager
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_appoint_store_owner_positive(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "testUser2").getData())

    def test_AppointStoreOwnerTwice(self):
        # store_id, assigner_id, assignee_name
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "testUser2").getData())
        # can't appoint owner twice
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "testUser2").isError())

    def test_AppointStoreOwnerNoStore(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(-1, self.user1_id, "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_owner(3, self.user1_id, "testUser2").isError())

    def test_AppointStoreOwnerNoOwner(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, -1, "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "Ori").isError())

    def test_AppointStoreOwnerNoPermission(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user2_id, "testUser3").isError())
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "Niv").isError())



if __name__ == '__main__':
    unittest.main()
