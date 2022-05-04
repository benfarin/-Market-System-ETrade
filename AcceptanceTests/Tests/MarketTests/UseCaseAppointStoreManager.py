import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseAppointStoreManager(unittest.TestCase):
    # use-case 4.6

    def setUp(self):
        self.proxy_market = MarketProxyBridge(MarketRealBridge())
        self.proxy_user = UserProxyBridge(UserRealBridge())

        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)

        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.owner_id = self.proxy_user.register("testUser", "1234", "0540000000", 123,[] ,"Israel", "Beer Sheva", "Rager", 1, "testBank")
        self.manager_id = self.proxy_user.register("testUser2", "4321", "0540000001", 124, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.proxy_user.login_member("testUser", "1234")
        self.proxy_user.login_member("testUser2", "4321")
        self.store_id = self.proxy_user.open_store("testStore", self.owner_id , 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000)

    def test_AppointStoreManagerPositive(self):
        # store_id, assigner_id, assignee_id
        self.assertEqual(self.proxy_market.appoint_store_manager(self.store_id, self.owner_id, self.manager_id), True)

    def test_AppointStoreManagerNoStore(self):
        self.assertRaises(Exception, self.proxy_market.appoint_store_manager(-1, self.owner_id, self.manager_id))

    def test_AppointStoreManagerNoOwner(self):
        self.assertRaises(Exception, self.proxy_market.appoint_store_manager(self.store_id, -1, self.manager_id))

    def test_AppointStoreManagerNoNewManager(self):
        self.assertRaises(Exception, self.proxy_market.appoint_store_manager(self.store_id, self.owner_id, -1))

    def test_AppointStoreManagerTwice(self):
        # user was already appointed
        self.proxy_market.appoint_store_manager(self.store_id, self.owner_id, self.manager_id)
        self.assertRaises(Exception, self.proxy_market.appoint_store_manager(self.store_id, self.owner_id, self.manager_id))

    def test_AppointStoreManagerNoPermission(self):
        self.assertRaises(Exception, self.proxy_market.appoint_store_manager(self.store_id, self.manager_id, self.manager_id))

if __name__ == '__main__':
    unittest.main()
