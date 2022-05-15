import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCasePurchaseProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.market_proxy = MarketProxyBridge(MarketRealBridge())
        cls.user_proxy = UserProxyBridge(UserRealBridge())
        cls.user_proxy.appoint_system_manager("user1", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                              "Ben Gurion", 1, 1)
        cls.__guestId = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                "Ben Gurion", 0, "HaPoalim")
        cls.user_id = cls.user_proxy.login_member(cls.__guestId, "user1", "1234").getData().getUserID()

        cls.store_0 = cls.user_proxy.open_store("s0", cls.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                0, "000000").getData().getStoreId()
        cls.store_1 = cls.user_proxy.open_store("s1", cls.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                0, "000000").getData().getStoreId()
        cls.store_2 = cls.user_proxy.open_store("s2", cls.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                0, "000000").getData().getStoreId()

        cls.product01 = cls.market_proxy.add_product_to_store(cls.store_0, cls.user_id, "Product-01", 100,
                                                              "Category", 8,["Test1", "Test2"]).getData().getProductId()
        cls.product02 = cls.market_proxy.add_product_to_store(cls.store_0, cls.user_id, "Product-02", 150,
                                                              "Category", 9,["Test1", "Test2"]).getData().getProductId()
        cls.product1 = cls.market_proxy.add_product_to_store(cls.store_1, cls.user_id, "Product-1", 100,
                                                             "Category", 10,["Test1", "Test2"]).getData().getProductId()
        cls.product2 = cls.market_proxy.add_product_to_store(cls.store_2, cls.user_id, "Product-2", 10,
                                                             "Category", 11,["Test1", "Test2"]).getData().getProductId()

        cls.market_proxy.add_quantity_to_store(cls.store_0, cls.user_id, cls.product01, 100)
        cls.market_proxy.add_quantity_to_store(cls.store_0, cls.user_id, cls.product02, 100)
        cls.market_proxy.add_quantity_to_store(cls.store_1, cls.user_id, cls.product1, 100)
        cls.market_proxy.add_quantity_to_store(cls.store_2, cls.user_id, cls.product2, 100)

    def test_purchase_positive1(self):
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 1)

        userTransaction = self.user_proxy.purchase_product(self.user_id, 500, 20)
        self.assertEqual(3310, userTransaction.getData().getTotalAmount())
        print(userTransaction)

    def test_guest_then_member_purchase(self):
        guest2_id = self.user_proxy.login_guest().getData().getUserID()

        self.user_proxy.add_product_to_cart(guest2_id, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(guest2_id, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(guest2_id, self.store_1, self.product1, 10)
        self.user_proxy.add_product_to_cart(guest2_id, self.store_2, self.product2, 1)

        self.user_proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, "HaPoalim")
        member2_id = self.user_proxy.login_member(guest2_id, "user2", "1234").getData().getUserID()

        userTransaction = self.user_proxy.purchase_product(member2_id, 500, 20)
        self.assertEqual(3310, userTransaction.getData().getTotalAmount())
        print(userTransaction)

    def test_login_logout_login_purchase(self):
        guest3_id = self.user_proxy.login_guest().getData().getUserID()

        self.user_proxy.add_product_to_cart(guest3_id, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(guest3_id, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(guest3_id, self.store_1, self.product1, 10)
        self.user_proxy.add_product_to_cart(guest3_id, self.store_2, self.product2, 1)

        self.user_proxy.register( "user3", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, "HaPoalim")
        member3_id = self.user_proxy.login_member(guest3_id,"user3", "1234").getData().getUserID()

        self.user_proxy.logout_member(member3_id)
        self.user_proxy.login_member(member3_id,"user3", "1234")

        userTransaction = self.user_proxy.purchase_product(member3_id, 500, 20)
        self.assertEqual(3310, userTransaction.getData().getTotalAmount())
        print(userTransaction)

    def test_two_user_trying_to_by_in_the_same_time(self):
        guest4_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register(guest4_id, "user4", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, "HaPoalim")
        member4_id = self.user_proxy.login_member("user3", "1234").getData().getUserID()

        self.user_proxy.add_product_to_cart(member4_id, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(member4_id, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(member4_id, self.store_1, self.product1, 10)
        self.user_proxy.add_product_to_cart(member4_id, self.store_2, self.product2, 1)

        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        t1 = ThreadWithReturn(target=self.user_proxy.purchase_product, args=(member4_id, 500, 20))
        t2 = ThreadWithReturn(target=self.user_proxy.purchase_product, args=(self.user_id, 50, 30))

        t1.start()
        t2.start()

        ut_1 = t1.join()
        ut_2 = t2.join()

        self.assertTrue(ut_1.getData().getTotalAmount() == 3310 and ut_2.getData().getTotalAmount() == 2240)
        print(ut_1)
        print(ut_2)

    def test_cart_clean(self):
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, 50, 30)
        ut_2 = self.user_proxy.purchase_product(self.user_id, 50, 30)
        self.assertTrue(ut_1.getData().getTotalAmount() == 2240 and ut_2.isError())
        print(ut_2.__str__())

    def test_purchas_empty_cart(self):
        ut_1 = self.user_proxy.purchase_product(self.user_id, 50, 30)
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())


if __name__ == '__main__':
    unittest.main()
