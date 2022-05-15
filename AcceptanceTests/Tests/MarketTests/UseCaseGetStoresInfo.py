import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseGetStoresInfo(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.proxy_market = MarketProxyBridge(MarketRealBridge())
        self.proxy_user = UserProxyBridge(UserRealBridge())
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva", "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register(self.__guestId1, "testUser", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        self.owner_id = self.proxy_user.login_member("testUser", "1234").getData().getUserID()
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id = self.proxy_user.open_store("testStore", self.owner_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()
        self.store_id1 = self.proxy_user.open_store("testStore1", self.owner_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register(self.__guestId2, "testUser2", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        self.manager_id = self.proxy_user.login_member("testUser2", "1234").getData().getUserID()
        self.proxy_market.appoint_store_manager(self.store_id, self.owner_id, self.manager_id)

    def test_get_stores_info_positive(self):
        print(self.proxy_market.get_store_info(self.store_id, self.owner_id).getData())
        self.assertTrue(True)

    def test_get_store_by_id(self):
       print(self.proxy_market.get_store_by_ID(self.store_id).getData())
       self.assertTrue(True)

    def test_get_all_stores(self):
        print(self.proxy_market.getAllStores().getData())
        self.assertTrue(True)

    def test_user_store(self):
        print(self.proxy_market.getUserStore(self.owner_id).getData())
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
