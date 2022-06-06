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
        admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(admin_id, "manager", "1234")

        # create 3 users
        self.__guestId = self.user_proxy.login_guest().getData().getUserID()
        self.__guestId2 = self.user_proxy.login_guest().getData().getUserID()
        self.__guestId3 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.user_proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        self.user_proxy.register("user3", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        # login 3 users
        self.user_id = self.user_proxy.login_member(self.__guestId, "user1", "1234").getData().getUserID()
        self.user_id2 = self.user_proxy.login_member(self.__guestId, "user2", "1234").getData().getUserID()
        self.user_id3 = self.user_proxy.login_member(self.__guestId, "user3", "1234").getData().getUserID()

        # create 3 stores
        self.store_0 = self.user_proxy.open_store("s0", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, 0).getData().getStoreId()
        self.store_1 = self.user_proxy.open_store("s1", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, 0).getData().getStoreId()
        self.store_2 = self.user_proxy.open_store("s2", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
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
        self.product2 = self.market_proxy.add_product_to_store(self.store_2, self.user_id, "Product-2", 10,
                                                               "Category", 11,
                                                               ["Test1", "Test2"]).getData().getProductId()

        self.market_proxy.add_quantity_to_store(self.store_0, self.user_id, self.product01, 100)
        self.market_proxy.add_quantity_to_store(self.store_0, self.user_id, self.product02, 100)
        self.market_proxy.add_quantity_to_store(self.store_1, self.user_id, self.product1, 100)
        self.market_proxy.add_quantity_to_store(self.store_2, self.user_id, self.product2, 100)

    def tearDown(self) -> None:
        # remove products from stores
        self.market_proxy.remove_product_from_store(self.store_0, self.user_id, self.product01)
        self.market_proxy.remove_product_from_store(self.store_0, self.user_id, self.product02)
        self.market_proxy.remove_product_from_store(self.store_1, self.user_id, self.product1)
        self.market_proxy.remove_product_from_store(self.store_2, self.user_id, self.product2)
        # remove stores
        self.market_proxy.removeStoreForGood(self.user_id, self.store_0)
        self.market_proxy.removeStoreForGood(self.user_id, self.store_1)
        self.market_proxy.removeStoreForGood(self.user_id, self.store_2)
        # remove users
        self.user_proxy.removeMember("manager", "user1")
        self.user_proxy.removeMember("manager", "user2")
        self.user_proxy.removeMember("manager", "user3")
        self.user_proxy.removeSystemManger_forTests("manager")

    def test_purchase_positive1(self):
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 1)

        # user_id, cardNumber, month, year, holderCardName, cvv, holderID
        userTransaction = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "27", "Rotem", "123", "123")
        self.assertEqual(3310, userTransaction.getData().getTotalAmount())
        print(userTransaction)


    def test_guest_then_member_purchase(self):
        guest2_id = self.user_proxy.login_guest().getData().getUserID()

        self.user_proxy.add_product_to_cart(guest2_id, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(guest2_id, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(guest2_id, self.store_1, self.product1, 10)
        self.user_proxy.add_product_to_cart(guest2_id, self.store_2, self.product2, 1)

        self.user_proxy.register("user2", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        member2_id = self.user_proxy.login_member(guest2_id, "user2", "1234").getData().getUserID()

        userTransaction = self.user_proxy.purchase_product(member2_id, "1234123412341234", "2", "27", "Rotem", "123", "123")
        self.assertEqual(3310, userTransaction.getData().getTotalAmount())
        print(userTransaction)

    def test_login_logout_login_purchase(self):
        guest3_id = self.user_proxy.login_guest().getData().getUserID()

        self.user_proxy.add_product_to_cart(guest3_id, self.store_0, self.product01, 20)
        self.user_proxy.add_product_to_cart(guest3_id, self.store_0, self.product02, 2)
        self.user_proxy.add_product_to_cart(guest3_id, self.store_1, self.product1, 10)
        self.user_proxy.add_product_to_cart(guest3_id, self.store_2, self.product2, 1)

        self.user_proxy.register("user3", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        member3_id = self.user_proxy.login_member(guest3_id, "user3", "1234").getData().getUserID()

        self.user_proxy.logout_member(member3_id)
        guest = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(guest, "user3", "1234")

        userTransaction = self.user_proxy.purchase_product(member3_id,"1234123412341234", "2", "27", "Rotem", "123", "123")
        self.assertEqual(3310, userTransaction.getData().getTotalAmount())
        print(userTransaction)

    def test_two_user_trying_to_by_in_the_same_time(self):
        guest4_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user4", "1234", "0500000000", 500, 20, "Israel", "Beer Sheva",
                                 "Ben Gurion", 0, 0)
        member4_id = self.user_proxy.login_member(guest4_id, "user3", "1234").getData().getUserID()

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

        ut_1 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "27", "Rotem", "123", "123")
        ut_2 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "27", "Rotem", "123", "123")
        self.assertTrue(ut_1.getData().getTotalAmount() == 2240 and ut_2.isError())
        print(ut_2.__str__())

    def test_purchas_empty_cart(self):
        ut_1 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "27", "Rotem", "123", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())

    # there is problem with threads, sometimes doesn't work

    def test_purchase_with_threads(self):
        t1 = ThreadWithReturn(target=self.user_proxy.add_product_to_cart,
                              args=(self.user_id2, self.store_0, self.product01, 100))
        t2 = ThreadWithReturn(target=self.user_proxy.add_product_to_cart,
                              args=(self.user_id3, self.store_0, self.product01, 100))
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        tran1 = self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")
        tran2 = self.user_proxy.purchase_product(self.user_id3,"1234123412341234", "2", "27", "Rotem", "123", "123")

        print(tran1)
        print(tran2)

        if tran1.isError():
            self.assertEqual(tran2.getData().getTotalAmount(), 10000.0)
        if tran2.isError():
            self.assertEqual(tran1.getData().getTotalAmount(), 10000.0)
        else:
            self.assertTrue(False)

    def test_purchase_with_thread2(self):
        t1 = []
        t2 = []
        for i in range(50):
            t1.append(ThreadWithReturn(target=self.user_proxy.add_product_to_cart,
                                     args=(self.user_id2, self.store_0, self.product01, 1)))
            t2.append(ThreadWithReturn(target=self.user_proxy.add_product_to_cart,
                                     args=(self.user_id3, self.store_0, self.product01, 1)))
        for i in range(50):
            t1[i].start()
            t2[i].start()

        for i in range(50):
            t1[i].join()
            t2[i].join()

        trans1 = self.user_proxy.purchase_product(self.user_id2, "1234123412341234", "2", "27", "Rotem", "123", "123")
        trans2 = self.user_proxy.purchase_product(self.user_id3, "1234123412341234", "2", "27", "Rotem", "123", "123")
        print(trans1)
        print(trans2)
        self.assertEqual(trans1.getData().getTotalAmount(), 5000.0)
        self.assertEqual(trans2.getData().getTotalAmount(), 5000.0)

    def test_fail_purchase_cart_cvvNotGood(self):
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "27", "Rotem", "123", "123")
        ut_2 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "27", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError()  and ut_2.isError())
        print(ut_1.__str__())
        print(ut_2.__str__())

    def test_fail_purchase_cart_cvvNotGood(self):
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "27", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())

    def test_fail_purchase_cart_CardNumberNotGood(self):
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "-12", "2", "27", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())

    def test_fail_purchase_cart_MonthNotGood(self): #check available month
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "-12", "27", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())

    def test_fail_purchase_cart_YearNotGood(self): #check avialable year
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "-1241", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())

    def test_fail_purchase_cart_ExpiredCard(self): # check if the date on the card is available.
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "2", "2000", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())

    def test_fail_purchase_cart_availableMonth(self): # month cant be 80
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "1234123412341234", "80", "2000", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())

    def test_fail_purchase_cart_availableCardNumber(self):  # CardNumber cant be 0
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "0", "80", "2000", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())

    def test_fail_purchase_cart_availableCardNumber2(self):  # CardNumber have to be 16 digits
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product01, 10)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_0, self.product02, 3)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_1, self.product1, 7)
        self.user_proxy.add_product_to_cart(self.user_id, self.store_2, self.product2, 9)

        ut_1 = self.user_proxy.purchase_product(self.user_id, "2342", "80", "2000", "Rotem", "0", "123")
        self.assertTrue(ut_1.isError())
        print(ut_1.__str__())


if __name__ == '__main__':
    unittest.main()
