import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseCloseStore(unittest.TestCase):
    # use-case 4.9
    @classmethod
    def setUpClass(self):
        self.proxy_market = MarketProxyBridge(MarketRealBridge())
        self.proxy_user = UserProxyBridge(UserRealBridge())
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register(self.__guestId1, "testUser", "1243", "0540000000", 123, [], "Israel", "Beer Sheva",
                                                "Rager", 1, "testBank")
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.user_id = self.proxy_user.login_member("testUser", "1243").getData().getUserID()
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva",
                                                   "Rager", 1, 00000).getData().getStoreId()

    def test_closeStorePositive_afterLogOut(self):
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1243")
        self.assertTrue(self.proxy_market.close_store(self.store_id, self.user_id).getData())

    def test_closeStorePositive(self):
        self.assertTrue(self.proxy_market.close_store(self.store_id, self.user_id).getData())
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1243")
        self.store_id1 = self.proxy_user.open_store("testStore", self.user_id, 123, None, "Israel", "Beer Sheva",
                                                   "Rager", 1, 00000).getData().getStoreId()
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1243")
        self.assertTrue(self.proxy_market.close_store(self.store_id1, self.user_id).getData())

    def test_closeStoreNegative(self):
        # store doesn't exist
        self.assertTrue(self.proxy_market.close_store(-1, self.user_id).isError())
        self.proxy_user.logout_member(self.user_id)
        self.proxy_user.login_member("testUser", "1243")
        self.assertTrue(self.proxy_market.close_store(-2, self.user_id).isError())



if __name__ == '__main__':
    unittest.main()
