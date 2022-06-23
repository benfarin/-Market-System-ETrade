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

        # create 3 users
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser", "1234", "0540000000", 123, 0, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "4321", "0540000001", 124, 1, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "4321", "0540000002", 124, 0, "Israel", "Beer Sheva",
                                "Rager", 1, 0)
        # login 3 users
        self.user1_id = self.proxy_user.login_member(self.__guestId1, "testUser", "1234").getData().getUserID()
        self.user2_id = self.proxy_user.login_member(self.__guestId2, "testUser2", "4321").getData().getUserID()
        self.user3_id = self.proxy_user.login_member(self.__guestId3, "testUser3", "4321").getData().getUserID()
        # create store
        self.store_id = self.proxy_user.open_store("testStore", self.user1_id, 123, 2, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()

    def tearDown(self):
        # remove store
        self.proxy_market.removeStoreForGood(self.user1_id, self.store_id)
        # remove users
        self.proxy_user.removeMember("Manager", "testUser")
        self.proxy_user.removeMember("Manager", "testUser2")
        self.proxy_user.removeMember("Manager", "testUser3")
        # remove system manager
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_appoint_store_owner_positive(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "testUser2").getData())
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "testUser3").getData())
        store = self.proxy_market.get_store_by_ID(self.store_id).getData()
        # get store's owners
        owners = store.getStoreOwners()
        for i in range(len(owners)):
            owners[i] = owners[i].getUserID()
        # check user2, user3 and user1 (founder) are the store's owners
        users= [self.user1_id, self.user2_id, self.user3_id]
        for owner in owners:
            self.assertTrue(owner in users)
        # check user2 can add products to store now
        prod = self.proxy_market.add_product_to_store(self.store_id, self.user2_id, "testProduct1", 10,
                                                       "testCategory", 15, ["test"]).getData()
        store = self.proxy_market.get_store_by_ID(self.store_id).getData()
        prod_in_store = store.getProducts()[prod.getProductId()]
        self.assertEqual(prod_in_store.getProductName(), prod.getProductName())
        # self.assertEqual(store.getProducts()[prod.getProductId()]

    def test_AppointStoreOwnerTwice(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "testUser2").getData())
        # can't appoint owner twice
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "testUser2").isError())
        store = self.proxy_market.get_store_by_ID(self.store_id).getData()
        # get store's owners
        owners = store.getStoreOwners()
        for i in range(len(owners)):
            owners[i] = owners[i].getUserID()
        # check user2 and user1 (founder) are the store's owners
        self.assertTrue(owners == [self.user1_id, self.user2_id])

    def test_AppointStoreOwnerWrongArgs(self):
        # no such store
        self.assertTrue(self.proxy_market.appoint_store_owner(-1, self.user1_id, "testUser2").isError())
        # no such founder
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, -1, "testUser2").isError())
        # no such user to assign
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user1_id, "Ori").isError())

    def test_AppointStoreOwnerNoPermission(self):
        # user2 has no permission to assign
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.user2_id, "testUser3").isError())




if __name__ == '__main__':
    unittest.main()
