import unittest

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

        self.store_id1 = self.proxy_user.open_store("testStore1", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()
        self.store_id2 = self.proxy_user.open_store("testStore2", self.user_id2, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()
        self.product_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
                                                                 "testCategory", 150, ["test"]).getData().getProductId()
        self.product_id_2 = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct2", 100,
                                                                   "testCategory1", 150,
                                                                   ["test"]).getData().getProductId()
        self.product_id_3 = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct3", 20,
                                                                   "testCategory", 150,
                                                                   ["test"]).getData().getProductId()

        self.product_id_4 = self.proxy_market.add_product_to_store(self.store_id2, self.user_id2, "testProduct4", 20,
                                                                   "testCategory1", 150,
                                                                   ["test"]).getData().getProductId()
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id, 100)
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id_2, 100)
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id_3, 100)
        self.proxy_market.add_quantity_to_store(self.store_id2, self.user_id2, self.product_id_4, 150)

    def test_createOwnerAgreement(self):
        ownerAgreement1 = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, self.user_id2).getData()
        self.proxy_user.acceptOwnerAgreement(self.user_id1,self.user_id2, self.store_id1, ownerAgreement1.get_ownerAgreementID())
        ownerAgreement1 = self.proxy_market.appoint_store_owner(self.store_id1, self.user_id1, self.user_id3).getData()
        self.proxy_user.acceptOwnerAgreement(self.user_id1, self.user_id3, self.store_id1,ownerAgreement1.get_ownerAgreementID())
        self.proxy_user.acceptOwnerAgreement(self.user_id2, self.user_id3, self.store_id1,ownerAgreement1.get_ownerAgreementID())

