import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Backend.Service.MemberService import MemberService
from Backend.Service.UserService import UserService


class UseCasePurchaseProduct(unittest.TestCase):
    # usecase 2.9
    market_proxy = MarketProxyBridge(MarketRealBridge())
    user_proxy = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign system manager
        self.user_proxy.appoint_system_manager("manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "manager", "1234")

        # create 4 users
        self.__guestId = self.user_proxy.login_guest().getData().getUserID()
        self.__guestId2 = self.user_proxy.login_guest().getData().getUserID()
        self.__guestId3 = self.user_proxy.login_guest().getData().getUserID()
        self.__guestId4 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.user_proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.user_proxy.register("user3", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.user_proxy.register("user4", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)

        # login 4 users
        self.user_id = self.user_proxy.login_member(self.__guestId, "user1", "1234").getData().getUserID()
        self.user_id2 = self.user_proxy.login_member(self.__guestId2, "user2", "1234").getData().getUserID()
        self.user_id3 = self.user_proxy.login_member(self.__guestId3, "user3", "1234").getData().getUserID()
        self.user_id4 = self.user_proxy.login_member(self.__guestId4, "user4", "1234").getData().getUserID()

        # create 3 stores
        self.store_0 = self.user_proxy.open_store("s0", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, 0).getData().getStoreId()
        self.store_1 = self.user_proxy.open_store("s1", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, 0).getData().getStoreId()
        self.store_2 = self.user_proxy.open_store("s2", self.user_id4, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, 0).getData().getStoreId()

        # add products to stores
        self.product01 = self.market_proxy.add_product_to_store(self.store_0, self.user_id, "Product-01", 100,
                                                                "Category", 8,
                                                                ["Test1", "Test2"]).getData().getProductId()
        self.product02 = self.market_proxy.add_product_to_store(self.store_0, self.user_id, "Product-02", 150,
                                                                "Category", 9,
                                                                ["Test1", "Test2"]).getData().getProductId()
        self.product1 = self.market_proxy.add_product_to_store(self.store_1, self.user_id, "Product-1", 100,
                                                               "Category", 10,
                                                               ["Test1", "Test2"]).getData().getProductId()
        self.product2 = self.market_proxy.add_product_to_store(self.store_2, self.user_id4, "Product-2", 10,
                                                               "Category", 11,
                                                               ["Test1", "Test2"]).getData().getProductId()

        self.market_proxy.add_quantity_to_store(self.store_0, self.user_id, self.product01, 100)
        self.market_proxy.add_quantity_to_store(self.store_0, self.user_id, self.product02, 100)
        self.market_proxy.add_quantity_to_store(self.store_1, self.user_id, self.product1, 100)
        self.market_proxy.add_quantity_to_store(self.store_2, self.user_id4, self.product2, 100)

    def tearDown(self) -> None:
        # remove stores
        self.market_proxy.removeStoreForGood(self.user_id, self.store_0)
        self.market_proxy.removeStoreForGood(self.user_id, self.store_1)
        self.market_proxy.removeStoreForGood(self.user_id4, self.store_2)
        # remove users
        self.user_proxy.removeMember("manager", "user1")
        self.user_proxy.removeMember("manager", "user2")
        self.user_proxy.removeMember("manager", "user3")
        self.user_proxy.removeMember("manager", "user4")
        self.user_proxy.removeSystemManger_forTests("manager")

    def test_purchase_founder_not_logged_in(self):
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_1, self.product1, 10)

        self.user_proxy.logout_member("user1")
        # user_id, cardNumber, month, year, holderCardName, cvv, holderID
        self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")
        notifications = self.user_proxy.get_member_notifications(self.user_id).getData()
        self.assertTrue(notifications.exists())

        guest = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(guest, "user1", "1234").getData().getUserID()
        self.user_proxy.exit_system(guest)


    def test_purchase_founder_logged_in(self):
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_1, self.product1, 10)

        # user_id, cardNumber, month, year, holderCardName, cvv, holderID
        self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")
        notifications = self.user_proxy.get_member_notifications(self.user_id).getData()
        self.assertFalse(notifications.exists())


    def test_purchase_several_founders_not_logged_in(self):
        self.market_proxy.appoint_store_owner(self.store_0, self.user_id, "user3")
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_1, self.product1, 10)

        self.user_proxy.logout_member("user1")
        self.user_proxy.logout_member("user3")
        # user_id, cardNumber, month, year, holderCardName, cvv, holderID
        self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")
        notifications_user_1 = self.user_proxy.get_member_notifications(self.user_id).getData()
        notifications_user_2 = self.user_proxy.get_member_notifications(self.user_id3).getData()
        self.assertTrue(notifications_user_1.exists())
        self.assertTrue(notifications_user_2.exists())
        guest = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(guest, "user1", "1234").getData().getUserID()
        self.user_proxy.login_member(guest, "user3", "1234").getData().getUserID()
        self.user_proxy.exit_system(guest)

    def test_purchase_several_founders_not_logged_in_and_logged_in(self):
        self.market_proxy.appoint_store_owner(self.store_0, self.user_id, "user3")
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_1, self.product1, 10)

        self.user_proxy.logout_member("user3")
        # user_id, cardNumber, month, year, holderCardName, cvv, holderID
        self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")
        notifications_user_1 = self.user_proxy.get_member_notifications(self.user_id).getData()
        notifications_user_2 = self.user_proxy.get_member_notifications(self.user_id3).getData()
        self.assertFalse(notifications_user_1.exists())
        self.assertTrue(notifications_user_2.exists())
        guest = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(guest, "user3", "1234").getData().getUserID()
        self.user_proxy.exit_system(guest)

    def test_purchase_only_owner_get_notifications(self):
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_1, self.product1, 10)


        self.user_proxy.logout_member("user1")
        # user_id, cardNumber, month, year, holderCardName, cvv, holderID
        self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")
        notifications_user_1 = self.user_proxy.get_member_notifications(self.user_id).getData()
        notifications_user_2 = self.user_proxy.get_member_notifications(self.user_id2).getData()
        notifications_user_3 = self.user_proxy.get_member_notifications(self.user_id3).getData()
        self.assertTrue(notifications_user_1.exists())
        self.assertFalse(notifications_user_2.exists())
        self.assertFalse(notifications_user_3.exists())
        guest = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(guest, "user1", "1234").getData().getUserID()
        self.user_proxy.exit_system(guest)

    def test_purchase_buy_from_several_stores(self):
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_1, self.product1, 10)
        self.user_proxy.add_product_to_cart(self.user_id2, self.store_2, self.product2, 1)

        self.user_proxy.logout_member("user1")
        self.user_proxy.logout_member("user4")
        # user_id, cardNumber, month, year, holderCardName, cvv, holderID
        self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")
        notifications_user_1 = self.user_proxy.get_member_notifications(self.user_id).getData()
        notifications_user_4 = self.user_proxy.get_member_notifications(self.user_id4).getData()
        self.assertTrue(notifications_user_1.exists())
        self.assertTrue(notifications_user_4.exists())

        guest = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(guest, "user1", "1234").getData().getUserID()
        self.user_proxy.login_member(guest, "user4", "1234").getData().getUserID()
        self.user_proxy.exit_system(guest)



if __name__ == '__main__':
    unittest.main()
