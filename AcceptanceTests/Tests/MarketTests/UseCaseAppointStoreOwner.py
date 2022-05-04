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
        cls.owner_id = cls.proxy_user.register("testUser", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        cls.manager_id = cls.proxy_user.register("testUser2", "4321", "0540000001", 124, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        cls.proxy_user.login_member("testUser", "1234")
        cls.proxy_user.login_member("testUser2", "4321")
        cls.store_id = cls.proxy_user.open_store("testStore", cls.owner_id, 123, 2, "Israel", "Beer Sheva", "Rager", 1, 00000)
        c = 1

    def test_AppointStoreOwnerPositive(self):
        # store_id, assigner_id, assignee_id
        self.assertEqual(self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, self.manager_id), True)

    def test_AppointStoreOwnerNoStore(self):
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(-1, self.owner_id, self.manager_id))

    def test_AppointStoreOwnerNoOwner(self):
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(self.store_id, -1, self.manager_id))

    def test_AppointStoreOwnerNoNewOwner(self):
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, self.manager_id))

    def test_AppointStoreOwnerTwice(self):
        # user was already appointed
        self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, self.manager_id)
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(self.store_id, self.owner_id, self.manager_id))

    def test_AppointStoreOwnerNoPermission(self):
        self.assertRaises(Exception, self.proxy_market.appoint_store_owner(self.store_id, self.manager_id, self.manager_id))


if __name__ == '__main__':
    unittest.main()
