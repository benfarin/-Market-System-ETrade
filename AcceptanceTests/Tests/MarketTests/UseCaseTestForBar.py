import unittest
from collections import Counter

from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseAppointStoreOwner(unittest.TestCase):
    def setUp(self):
        self.proxy_market = MarketProxyBridge(MarketRealBridge())
        self.proxy_user = UserProxyBridge(UserRealBridge())

    def test_for_bar_6_users(self):
        guestId1 = self.proxy_user.login_guest().getData().getUserID()
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        guestId3 = self.proxy_user.login_guest().getData().getUserID()
        guestId4 = self.proxy_user.login_guest().getData().getUserID()
        guestId5 = self.proxy_user.login_guest().getData().getUserID()
        guestId6 = self.proxy_user.login_guest().getData().getUserID()

        self.proxy_user.register("AdminUser", "1234", "0540000000", 123, 0, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.proxy_user.register("testUser2", "4321", "0540000001", 124, 1, "Israel", "Beer Sheva", "Rager", 2, 1)
        self.proxy_user.register("testUser3", "4321", "0540000002", 125, 0, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.proxy_user.register("testUser4", "4321", "0540000004", 126, 4, "Israel", "Tel aviv", "Rager", 1,2)
        self.proxy_user.register("testUser5", "4321", "0540000005", 127, 2, "Israel", "Tel aviv", "Rager", 2, 3)
        self.proxy_user.register("testUser6", "4321", "0540000006", 128, 3, "Israel", "Tel aviv", "Rager", 1, 0)

        self.proxy_user.appoint_system_manager("AdminUser", "1234", "0500000000", 123, 0, "Israel",
                                               "Beer Sheva", "Rager", 1, 0)

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        u1_id = self.proxy_user.login_member(guestId1, "AdminUser", "1234").getData().getUserID()
        u2_id = self.proxy_user.login_member(guestId2, "testUser2", "4321").getData().getUserID()
        u3_id = self.proxy_user.login_member(guestId3, "testUser3", "4321").getData().getUserID()
        u4_id = self.proxy_user.login_member(guestId4, "testUser4", "4321").getData().getUserID()
        u5_id = self.proxy_user.login_member(guestId5, "testUser5", "4321").getData().getUserID()
        u6_id = self.proxy_user.login_member(guestId6, "testUser6", "4321").getData().getUserID()

        s1_id = self.proxy_user.open_store("Bar's Store", u2_id, 123, 2, "Israel", "Beer Sheva", "Rager",
                                                   1, 00000).getData().getStoreId()
        p_id = self.proxy_market.add_product_to_store(s1_id, u2_id, "Bamba", 30, "snacks",
                                                      0.300, ["Osem"]).getData().getProductId()
        self.proxy_market.add_quantity_to_store(s1_id, u2_id, p_id, 20)
        self.proxy_market.appoint_store_manager(s1_id, u2_id, "testUser3")
        self.proxy_market.set_stock_manager_perm(s1_id, u2_id, "testUser3")
        self.proxy_market.appoint_store_owner(s1_id, u2_id, "testUser4")
        self.proxy_market.appoint_store_owner(s1_id, u2_id, "testUser5")
        self.proxy_user.logout_member("testUser5")

        storeDTO = self.proxy_market.get_store_by_ID(s1_id).getData()
        storeOwnersIds = [storeOwner.getUserID() for storeOwner in storeDTO.getStoreOwners()]
        self.assertEqual(Counter(storeOwnersIds), Counter([u2_id, u4_id, u5_id]))
        storeMangersIds = [storeManger.getUserID() for storeManger in storeDTO.getStoreManagers()]
        self.assertEqual(Counter(storeMangersIds), Counter([u3_id]))
        products = [product.getProductId() for product in storeDTO.getProducts().values()]
        self.assertEqual(products, [p_id])
        self.assertTrue(self.proxy_user.logout_member("testUser5").isError())

        self.proxy_market.removeStoreForGood(u2_id, s1_id)
        self.proxy_user.removeMember("AdminUser", "testUser2")  #can be done only because the store has deleted!
        self.proxy_user.removeMember("AdminUser", "testUser3")
        self.proxy_user.removeMember("AdminUser", "testUser4")
        self.proxy_user.removeMember("AdminUser", "testUser5")
        self.proxy_user.removeMember("AdminUser", "testUser6")
        self.proxy_user.removeSystemManger_forTests("AdminUser")

    def test_for_bar_3_appoints(self):
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        guestId = self.proxy_user.login_guest().getData().getUserID()
        guestId1 = self.proxy_user.login_guest().getData().getUserID()
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        guestId3 = self.proxy_user.login_guest().getData().getUserID()
        guestId4 = self.proxy_user.login_guest().getData().getUserID()

        self.proxy_user.register("testUser", "1234", "0540000000", 123, 0, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.proxy_user.register("testUser2", "4321", "0540000001", 124, 1, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.proxy_user.register("testUser3", "4321", "0540000002", 124, 0, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.proxy_user.register("testUser4", "4321", "0540000003", 124, 2, "Israel", "Tel aviv",
                                 "Rager", 1, 0)

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.proxy_user.login_member(guestId, "Manager", "1234").getData().getUserID()
        user1_id = self.proxy_user.login_member(guestId1, "testUser", "1234").getData().getUserID()
        user2_id = self.proxy_user.login_member(guestId2, "testUser2", "4321").getData().getUserID()
        user3_id = self.proxy_user.login_member(guestId3, "testUser3", "4321").getData().getUserID()
        user4_id = self.proxy_user.login_member(guestId4, "testUser4", "4321").getData().getUserID()
        store_id = self.proxy_user.open_store("testStore", user1_id, 123, 2, "Israel", "Beer Sheva", "Rager",
                                              1, 00000).getData().getStoreId()

        self.proxy_market.appoint_store_owner(store_id, user1_id, "testUser2")
        self.proxy_market.appoint_store_owner(store_id, user2_id, "testUser3")
        self.proxy_market.appoint_store_owner(store_id, user3_id, "testUser4")
        storeOwnersDTOs = self.proxy_market.get_store_by_ID(store_id).getData().getStoreOwners()
        storeOwnersIds = [storeOwner.getUserID() for storeOwner in storeOwnersDTOs]
        self.assertEqual(Counter(storeOwnersIds), Counter([user1_id, user2_id, user3_id, user4_id]))

        self.proxy_market.removeStoreOwner(store_id, user1_id, "testUser2")
        storeOwnersDTOs = self.proxy_market.get_store_by_ID(store_id).getData().getStoreOwners()
        storeOwnersIds = [storeOwner.getUserID() for storeOwner in storeOwnersDTOs]
        self.assertEqual(storeOwnersIds, [user1_id])

        self.proxy_market.removeStoreForGood(user1_id, store_id)
        self.proxy_user.removeMember("Manager", "testUser")
        self.proxy_user.removeMember("Manager", "testUser2")  #can be done only because the store has deleted!
        self.proxy_user.removeMember("Manager", "testUser3")
        self.proxy_user.removeMember("Manager", "testUser4")
        self.proxy_user.removeSystemManger_forTests("Manager")


if __name__ == '__main__':
    unittest.main()
