import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseAppointStoreOwner(unittest.TestCase):
    # use-case 4.4
    @classmethod
    def setUpClass(cls):
        cls.proxy_market = MarketProxyBridge(MarketRealBridge())
        cls.proxy_user = UserProxyBridge(UserRealBridge())
        cls.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        cls.__guestId1 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        cls.__guestId2 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser2", "4321", "0540000001", 124, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        cls.__guestId3 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser3", "4321", "0540000002", 124, [], "Israel", "Beer Sheva",
                                "Rager", 1, "testBank")
        cls.__guestId4 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser4", "4321", "0540000003", 124, [], "Israel", "Tel aviv",
                                "Rager", 1, "testBank")

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        cls.owner_id = cls.proxy_user.login_member(cls.__guestId1, "testUser", "1234").getData().getUserID()
        cls.manager_id1 = cls.proxy_user.login_member(cls.__guestId2, "testUser2", "4321").getData().getUserID()
        cls.manager_id2 = cls.proxy_user.login_member(cls.__guestId3, "testUser3", "4321").getData().getUserID()
        cls.manager_id3 = cls.proxy_user.login_member(cls.__guestId4, "testUser4", "4321").getData().getUserID()
        cls.store_id = cls.proxy_user.open_store("testStore", cls.owner_id, 123, 2, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()

    def test_AppointStoreOwnerPositive(self):
        # store_id, assigner_id, assignee_name
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, "testUser2").getData())
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, "testUser3").getData())

    def test_AppointStoreOwnerNoStore(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(-1, self.owner_id, "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_owner(-2, self.owner_id, "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_owner(-1, self.owner_id, "").isError())

    def test_AppointStoreOwnerNoOwner(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, -1, "testUser2").isError())
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, -1, "").isError())
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, -1, "egeadasd").isError())

    def test_AppointStoreOwnerNoNewOwner(self):
        self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, "testUser2")
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, "testUser2").isError())

    def test_AppointStoreOwnerTwice(self):
        # user was already appointed
        self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, "testUser2")
        self.assertRaises(Exception,self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, "testUser2").getError())
        self.proxy_user.logout_member(self.owner_id)
        self.proxy_user.login_member(self.owner_id, "testUser", "1234")
        self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, "testUser3")
        self.assertRaises(Exception,self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, "testUser3").getError())

    def test_AppointStoreOwnerNoPermission(self):
        self.assertTrue(self.proxy_market.appoint_store_owner(self.store_id, self.manager_id1, "testUser2").isError())
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(self.store_id, self.manager_id1, "testUser2").getError())
        self.proxy_user.logout_member(self.manager_id1)
        self.proxy_user.login_member(self.manager_id1, "testUser2", "4321")
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(self.store_id, self.manager_id1, "testUser3").getError())
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(self.store_id, self.manager_id1, "testUser4").getError())
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(self.store_id, self.manager_id1, "").getError())


if __name__ == '__main__':
    unittest.main()
