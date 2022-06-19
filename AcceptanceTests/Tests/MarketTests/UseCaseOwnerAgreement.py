import unittest
from collections import Counter

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class MyTestCase(unittest.TestCase):
    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "Manager", "1234")
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser1", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.user_id1 = self.proxy_user.login_member(self.__guestId1, "testUser1", "1234").getData().getUserID()
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "12345", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.user_id2 = self.proxy_user.login_member(self.__guestId2, "testUser2", "12345").getData().getUserID()
        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "123456", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.user_id3 = self.proxy_user.login_member(self.__guestId3, "testUser3", "123456").getData().getUserID()
        self.__guestId4 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser4", "123456", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.user_id4 = self.proxy_user.login_member(self.__guestId4, "testUser4", "123456").getData().getUserID()

        self.store_id1 = self.proxy_user.open_store("testStore1", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()

    def test_createOwnerAgreement(self):
        ownerAgreement = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser2").getData()
        self.assertTrue(ownerAgreement.getIsAccepted())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2]))

        ownerAgreement1_id = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id2,
                                                                   "testUser3").getData().getOwnerAgreementId()
        self.assertFalse(self.proxy_user.getOwnerAgreementById(self.store_id1,
                                                               ownerAgreement1_id).getData().getIsAccepted())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2]))
        self.assertTrue(self.proxy_user.acceptOwnerAgreement(self.user_id1, self.store_id1,ownerAgreement1_id).getData())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2, self.user_id3]))

    def test_ownerAgreement_reject(self):
        ownerAgreement = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser2").getData()
        self.assertTrue(ownerAgreement.getIsAccepted())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2]))

        ownerAgreement1 = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id2, "testUser3").getData()
        self.assertFalse(ownerAgreement1.getIsAccepted())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2]))
        self.assertTrue(self.proxy_user.rejectOwnerAgreement(self.user_id1, self.store_id1,
                                                             ownerAgreement1.getOwnerAgreementId()).getData())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2]))

    def test_ownerAgreement_accept_and_reject(self):
        self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser2").getData()

        ownerAgreement1 = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id2, "testUser3").getData()
        self.assertTrue(self.proxy_user.acceptOwnerAgreement(self.user_id1, self.store_id1,
                                                             ownerAgreement1.getOwnerAgreementId()).getData())

        ownerAgreement2 = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser4").getData()
        self.assertTrue(self.proxy_user.acceptOwnerAgreement(self.user_id2, self.store_id1,
                                                             ownerAgreement2.getOwnerAgreementId()).getData())
        self.assertTrue(self.proxy_user.rejectOwnerAgreement(self.user_id3, self.store_id1,
                                                             ownerAgreement2.getOwnerAgreementId()).getData())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2, self.user_id3]))

    def test_chain_of_owners_then_delete_in_new_appoint(self):
        self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser2").getData()

        ownerAgreement = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id2, "testUser3").getData()
        self.assertTrue(self.proxy_user.acceptOwnerAgreement(self.user_id1, self.store_id1,
                                                             ownerAgreement.getOwnerAgreementId()).getData())

        ownerAgreement1 = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id3, "testUser4").getData()
        self.assertTrue(self.proxy_user.acceptOwnerAgreement(self.user_id1, self.store_id1,
                                                             ownerAgreement1.getOwnerAgreementId()).getData())
        self.proxy_market.removeStoreOwner(self.store_id1, self.user_id2, "testUser3")
        self.assertTrue(self.proxy_user.acceptOwnerAgreement(self.user_id2, self.store_id1,
                                                             ownerAgreement1.getOwnerAgreementId()).isError())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2]))

    def test_AppointStoreOwnerTwice(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser2").getData())
        # can't appoint owner twice
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser2").isError())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2]))

    def test_towAppoints(self):
        self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser2").getData()

        ownerAgreement1 = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser3").getData()
        ownerAgreement2 = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, "testUser4").getData()
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()), Counter([self.user_id1, self.user_id2]))

        assigneesIds = [ownerAgreement.getAssignee().getUserID()
                        for ownerAgreement in self.proxy_user.getAllStoreOwnerAgreements(self.store_id1).getData()]
        isAceppteds = [ownerAgreement.getIsAccepted()
                        for ownerAgreement in self.proxy_user.getAllStoreOwnerAgreements(self.store_id1).getData()]
        self.assertEqual(Counter(assigneesIds), Counter([self.user_id3, self.user_id4]))
        self.assertEqual(isAceppteds, [False, False])

        self.proxy_user.acceptOwnerAgreement(self.user_id2, self.store_id1, ownerAgreement2.getOwnerAgreementId())
        assigneesIds = [ownerAgreement.getAssignee().getUserID()
                        for ownerAgreement in self.proxy_user.getAllStoreOwnerAgreements(self.store_id1).getData()]
        self.assertEqual(assigneesIds, [self.user_id3])

        self.proxy_user.acceptOwnerAgreement(self.user_id2, self.store_id1, ownerAgreement1.getOwnerAgreementId())
        self.assertEqual(Counter(self.__getAllStoreOwnersIds()),
                         Counter([self.user_id1, self.user_id2, self.user_id3, self.user_id4]))

    def tearDown(self):
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id1)
        self.proxy_market.remove_member("Manager", "testUser4")
        self.proxy_market.remove_member("Manager", "testUser3")
        self.proxy_market.remove_member("Manager", "testUser2")
        self.proxy_market.remove_member("Manager", "testUser1")
        self.proxy_user.removeSystemManger_forTests("Manager")

    def __getAllStoreOwnersIds(self):
        storeOwnersDTOs = self.proxy_market.get_store_by_ID(self.store_id1).getData().getStoreOwners()
        return [storeOwner.getUserID() for storeOwner in storeOwnersDTOs]


if __name__ == '__main__':
    unittest.main()
