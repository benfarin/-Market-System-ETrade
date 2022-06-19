import unittest
from collections import Counter

from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseForBar(unittest.TestCase):
    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign system manager
        self.proxy_user.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "manager", "1234")

        self.u2_id = -1
        self.s1_id = -1

    def tearDown(self):
        self.proxy_market.removeStoreForGood(self.u2_id, self.s1_id)
        self.proxy_user.removeMember("manager","Rotem")
        self.proxy_user.removeMember("manager", "Kfir")
        self.proxy_user.removeMember("manager", "Ori")
        self.proxy_user.removeMember("manager", "Bar")
        self.proxy_user.removeMember("manager", "Niv")
        self.proxy_user.removeSystemManger_forTests("AdminUser")
        self.proxy_user.removeSystemManger_forTests("manager")

    def test_for_bar_6_users(self):
        # create 6 user - one of them will be a system manager
        guestId1 = self.proxy_user.login_guest().getData().getUserID()
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        guestId3 = self.proxy_user.login_guest().getData().getUserID()
        guestId4 = self.proxy_user.login_guest().getData().getUserID()
        guestId5 = self.proxy_user.login_guest().getData().getUserID()
        guestId6 = self.proxy_user.login_guest().getData().getUserID()

        self.proxy_user.register("AdminUser", "1234", "0540000000", 123, 0, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.proxy_user.register("Rotem", "4321", "0540000001", 124, 1, "Israel", "Beer Sheva", "Rager", 2, 1)
        self.proxy_user.register("Kfir", "4321", "0540000002", 125, 0, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.proxy_user.register("Ori", "4321", "0540000004", 126, 4, "Israel", "Tel aviv", "Rager", 1,2)
        self.proxy_user.register("Bar", "4321", "0540000005", 127, 2, "Israel", "Tel aviv", "Rager", 2, 3)
        self.proxy_user.register("Niv", "4321", "0540000006", 128, 3, "Israel", "Tel aviv", "Rager", 1, 0)

        self.proxy_user.appoint_system_manager("AdminUser", "1234", "0500000000", 123, 0, "Israel",
                                               "Beer Sheva", "Rager", 1, 0)

        # login 6 users
        u1_id = self.proxy_user.login_member(guestId1, "AdminUser", "1234").getData().getUserID()
        self.u2_id = self.proxy_user.login_member(guestId2, "Rotem", "4321").getData().getUserID()
        u3_id = self.proxy_user.login_member(guestId3, "Kfir", "4321").getData().getUserID()
        u4_id = self.proxy_user.login_member(guestId4, "Ori", "4321").getData().getUserID()
        u5_id = self.proxy_user.login_member(guestId5, "Bar", "4321").getData().getUserID()
        u6_id = self.proxy_user.login_member(guestId6, "Niv", "4321").getData().getUserID()

        # Rotem open store
        self.s1_id = self.proxy_user.open_store("Rotem's Store", self.u2_id, 123, 2, "Israel", "Beer Sheva", "Rager",
                                                   1, 00000).getData().getStoreId()
        # add products to store
        p_id = self.proxy_market.add_product_to_store(self.s1_id, self.u2_id, "Bamba", 30, "snacks",
                                                      0.300, ["Osem"]).getData().getProductId()
        # add product's quantity to store
        self.proxy_market.add_quantity_to_store(self.s1_id, self.u2_id, p_id, 20)
        # assign Kfir to be a store manager
        self.proxy_market.appoint_store_manager(self.s1_id, self.u2_id, "Kfir")
        # assign Kfir with stock permission
        self.proxy_market.set_stock_manager_perm(self.s1_id, self.u2_id, "Kfir")
        # assign Ori and Bar to be store's owners
        self.proxy_market.appoint_store_owner(self.s1_id, self.u2_id, "Ori")
        self.proxy_market.appoint_store_owner(self.s1_id, self.u2_id, "Bar")
        # Bar logout
        self.proxy_user.logout_member("Bar")

        storeDTO = self.proxy_market.get_store_by_ID(self.s1_id).getData()
        # get store owners
        storeOwnersIds = [storeOwner.getUserID() for storeOwner in storeDTO.getStoreOwners()]
        # check the owners are Rotem , Ori and Bar
        self.assertEqual(Counter(storeOwnersIds), Counter([self.u2_id, u4_id, u5_id]))
        # check the store manager is Kfir
        storeMangersIds = [storeManger.getUserID() for storeManger in storeDTO.getStoreManagers()]
        self.assertEqual(Counter(storeMangersIds), Counter([u3_id]))
        # check product1 is the only product in the store
        products = [product.getProductId() for product in storeDTO.getProducts().values()]
        self.assertEqual(products, [p_id])
        # Bar is already loged-out
        self.assertTrue(self.proxy_user.logout_member("Bar").isError())

    def test_for_bar_3_appoints(self):
        # create 4 users
        guestId1 = self.proxy_user.login_guest().getData().getUserID()
        guestId2 = self.proxy_user.login_guest().getData().getUserID()
        guestId3 = self.proxy_user.login_guest().getData().getUserID()
        guestId4 = self.proxy_user.login_guest().getData().getUserID()

        self.proxy_user.register("Ori", "1234", "0540000000", 123, 0, "Israel", "Beer Sheva", "Rager", 1, 0)
        self.proxy_user.register("Bar", "4321", "0540000001", 124, 1, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.proxy_user.register("Rotem", "4321", "0540000002", 124, 0, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.proxy_user.register("Kfir", "4321", "0540000003", 124, 2, "Israel", "Tel aviv",
                                 "Rager", 1, 0)

        # login 4 users
        self.u2_id = self.proxy_user.login_member(guestId1, "Ori", "1234").getData().getUserID()
        user2_id = self.proxy_user.login_member(guestId2, "Bar", "4321").getData().getUserID()
        user3_id = self.proxy_user.login_member(guestId3, "Rotem", "4321").getData().getUserID()
        user4_id = self.proxy_user.login_member(guestId4, "Kfir", "4321").getData().getUserID()
        # create a store
        store_id = self.proxy_user.open_store("Ori's Store", self.u2_id, 123, 2, "Israel", "Beer Sheva", "Rager",
                                              1, 00000).getData().getStoreId()
        # appoint Bar Rotem and Kfir to e store-owners
        self.proxy_market.appoint_store_owner(store_id, self.u2_id, "Bar")
        self.proxy_market.appoint_store_owner(store_id, user2_id, "Rotem")
        self.proxy_market.appoint_store_owner(store_id, user3_id, "Kfir")
        # check the owners are Ori, Rotem, Kfir and Bar
        storeOwnersDTOs = self.proxy_market.get_store_by_ID(store_id).getData().getStoreOwners()
        storeOwnersIds = [storeOwner.getUserID() for storeOwner in storeOwnersDTOs]
        self.assertEqual(Counter(storeOwnersIds), Counter([self.u2_id, user2_id, user3_id, user4_id]))

        # remove Bar as a store owner
        self.proxy_market.removeStoreOwner(store_id, self.u2_id, "Bar")
        # check the owners changed (only Ori - because Bar assigned Rotem and Rotem assigned Kfir the all should also be removed!)
        storeOwnersDTOs = self.proxy_market.get_store_by_ID(store_id).getData().getStoreOwners()
        storeOwnersIds = [storeOwner.getUserID() for storeOwner in storeOwnersDTOs]
        self.assertEqual(storeOwnersIds, [self.u2_id])

if __name__ == '__main__':
    unittest.main()
