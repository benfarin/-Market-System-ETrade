import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UsePurchasesHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proxy_market = MarketProxyBridge(MarketRealBridge())
        cls.proxy_user = UserProxyBridge(UserRealBridge())
        cls.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva", "Ben Gurion", 1, 1)
        cls.__guestId1 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser", "1234", "0540000000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        cls.owner_id = cls.proxy_user.login_member(cls.__guestId1, "testUser", "1234").getData().getUserID()
        cls.store_id = cls.proxy_user.open_store("testStore", cls.owner_id, 123, None, "Israel", "Beer Sheva", "Rager", 1, 00000).getData().getStoreId()
        cls.prod1 = cls.proxy_market.add_product_to_store(cls.store_id, cls.owner_id, "testProduct1", 10, "testCategory", 10, ["testKeyWord"]).getData()
        cls.proxy_market.add_quantity_to_store(cls.store_id, cls.owner_id, cls.prod1.getProductId(), 100)
        cls.prod2 = cls.proxy_market.add_product_to_store(cls.store_id, cls.owner_id, "testProduct2", 50, "testCategory", 10, ["testKeyWord"]).getData()
        cls.proxy_market.add_quantity_to_store(cls.store_id, cls.owner_id, cls.prod2.getProductId(), 100)
        cls.__guestId2 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser2", "1234", "0540030000", 123, [], "Israel", "Beer Sheva", "Rager", 1, "testBank")
        cls.user_id = cls.proxy_user.login_member(cls.__guestId2, "testUser2", "1234").getData().getUserID()
        cls.proxy_user.add_product_to_cart(cls.user_id, cls.store_id, cls.prod1.getProductId(), 12)
        cls.proxy_user.add_product_to_cart(cls.user_id, cls.store_id, cls.prod2.getProductId(), 3)

    def test_get_purchases_history(self):
        print(self.proxy_market.get_cart(self.user_id).__str__())


if __name__ == '__main__':
    unittest.main()
