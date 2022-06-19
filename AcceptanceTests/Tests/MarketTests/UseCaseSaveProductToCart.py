import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseSaveProductToCart(unittest.TestCase):
    databases = {'testing'}
    market_proxy = MarketProxyBridge(MarketRealBridge())
    user_proxy = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign system manager
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(self.admin_id, "Manager", "1234")
        # --------------------------users register ------------------------------------
        self.__guestId1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "053643643", "500", "20", "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        self.__guestId2 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user2", "12345", "0500000000", "505", "21", "Israel", "Tel aviv",
                                "Ben Gurion", 0, 0)
        self.__guestId3 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user3", "123451", "05325235", "506", "22", "Israel", "Tel aviv",
                                "Ben Gurion", 0, 0)
        self.__guestId4 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user4", "123452", "0503643342", "402", "2124", "Israel", "Tel aviv",
                                "Ben Gurion", 0, 0)
        self.__guestId5 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user5", "123456", "05043523523", "505", "21", "Israel", "ashdod",
                                "Ben Gurion", 0, 0)

        # ----------------------------user login --------------------------------------
        self.user_id1 = self.user_proxy.login_member(self.__guestId1, "user1", "1234").getData().getUserID()
        self.user_id2 = self.user_proxy.login_member(self.__guestId2, "user2", "12345").getData().getUserID()
        self.user_id3 = self.user_proxy.login_member(self.__guestId3, "user3", "123451").getData().getUserID()
        self.user_id4 = self.user_proxy.login_member(self.__guestId4, "user4", "123452").getData().getUserID()
        self.user_id5 = self.user_proxy.login_member(self.__guestId5, "user5", "123456").getData().getUserID()

        # ------------------------------------open stores-----------------------------------------------------
        self.store_id1 = self.user_proxy.open_store("store1", self.user_id1, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                    0, "000000").getData().getStoreId()
        self.store_id2 = self.user_proxy.open_store("store2", self.user_id2, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                    0, "000000").getData().getStoreId()
        self.store_id3 = self.user_proxy.open_store("store3", self.user_id3, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                    0, "000000").getData().getStoreId()
        self.store_id4 = self.user_proxy.open_store("store4", self.user_id4, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                    0, "000000").getData().getStoreId()
        self.store_id5 = self.user_proxy.open_store("store5", self.user_id5, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                    0, "000000").getData().getStoreId()

        self.store_id6 = self.user_proxy.open_store("store6", self.user_id1, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                    0, "000000").getData().getStoreId()
        self.store_id7 = self.user_proxy.open_store("store7", self.user_id2, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                    0, "000000").getData().getStoreId()
        self.store_id8 = self.user_proxy.open_store("store8", self.user_id3, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                    0, "000000").getData().getStoreId()

        # ------------------------------------------- products ----------------------------------------------------
        self.product1 = self.market_proxy.add_product_to_store(self.store_id1, self.user_id1, "Milk 5%", 500,
                                                             "Milky", 10, ["Milk", "Tara", "5%"]).getData()
        self.product2 = self.market_proxy.add_product_to_store(self.store_id1, self.user_id1, "Chocolate", 500,
                                                             "Milky", 15, ["Test1", "Test2"]).getData()

        self.product3 = self.market_proxy.add_product_to_store(self.store_id2, self.user_id2, "Product", 500,
                                                             "Category", 7, ["Test1", "Test2"]).getData()
        self.product4 = self.market_proxy.add_product_to_store(self.store_id2, self.user_id2, "Product", 500,
                                                             "Category", 9, ["Test1", "Test2"]).getData()

        self.product5 = self.market_proxy.add_product_to_store(self.store_id3, self.user_id3, "Product", 500,
                                                             "Category", 30, ["Test1", "Test2"]).getData()
        self.product6 = self.market_proxy.add_product_to_store(self.store_id3, self.user_id3, "Product", 500,
                                                             "Category", 1, ["Test1", "Test2"]).getData()

        self.product7 = self.market_proxy.add_product_to_store(self.store_id4, self.user_id4, "Product", 500,
                                                             "Category", 8, ["Test1", "Test2"]).getData()
        self.product8 = self.market_proxy.add_product_to_store(self.store_id4, self.user_id4, "Product", 500,
                                                             "Category", 10, ["Test1", "Test2"]).getData()

        self.product9 = self.market_proxy.add_product_to_store(self.store_id2, self.user_id2, "Product", 500,
                                                             "Category", 10, ["Test1", "Test2"]).getData()
        self.product10 = self.market_proxy.add_product_to_store(self.store_id5, self.user_id5, "Product", 500,
                                                              "Category", 10, ["Test1", "Test2"]).getData()

        self.product11 = self.market_proxy.add_product_to_store(self.store_id6, self.user_id1, "Product", 500,
                                                              "Category", 12, ["Test1", "Test2"]).getData()
        self.product12 = self.market_proxy.add_product_to_store(self.store_id6, self.user_id1, "Product", 500,
                                                              "Category", 18, ["Test1", "Test2"]).getData()

        self.product13 = self.market_proxy.add_product_to_store(self.store_id7, self.user_id2, "Product", 500,
                                                              "Category", 20, ["Test1", "Test2"]).getData()
        self.product14 = self.market_proxy.add_product_to_store(self.store_id7, self.user_id2, "Product", 500,
                                                              "Category", 22, ["Test1", "Test2"]).getData()

        self.product15 = self.market_proxy.add_product_to_store(self.store_id8, self.user_id3, "Product", 500,
                                                              "Category", 24, ["Test1", "Test2"]).getData()
        self.product16 = self.market_proxy.add_product_to_store(self.store_id8, self.user_id3, "Product", 500,
                                                              "Category", 5, ["Test1", "Test2"]).getData()

        # ----------------------------------------- add quantity to stores ----------------------------------------

        # store 1
        self.market_proxy.add_quantity_to_store(self.store_id1, self.user_id1, self.product1.getProductId(), 100)
        self.market_proxy.add_quantity_to_store(self.store_id1, self.user_id1, self.product2.getProductId(), 50)
        self.market_proxy.add_quantity_to_store(self.store_id1, self.user_id1, self.product3.getProductId(), 45)
        self.market_proxy.add_quantity_to_store(self.store_id1, self.user_id1, self.product4.getProductId(), 80)
        self.market_proxy.add_quantity_to_store(self.store_id1, self.user_id1, self.product5.getProductId(), 70)
        # store 2
        self.market_proxy.add_quantity_to_store(self.store_id2, self.user_id2, self.product3.getProductId(), 120)
        self.market_proxy.add_quantity_to_store(self.store_id2, self.user_id2, self.product9.getProductId(), 100)
        self.market_proxy.add_quantity_to_store(self.store_id2, self.user_id2, self.product7.getProductId(), 75)
        self.market_proxy.add_quantity_to_store(self.store_id2, self.user_id2, self.product8.getProductId(), 110)
        self.market_proxy.add_quantity_to_store(self.store_id2, self.user_id2, self.product1.getProductId(), 90)
        # store 3
        self.market_proxy.add_quantity_to_store(self.store_id3, self.user_id3, self.product1.getProductId(), 140)
        self.market_proxy.add_quantity_to_store(self.store_id3, self.user_id3, self.product1.getProductId(), 120)
        self.market_proxy.add_quantity_to_store(self.store_id3, self.user_id3, self.product1.getProductId(), 170)
        self.market_proxy.add_quantity_to_store(self.store_id3, self.user_id3, self.product1.getProductId(), 170)
        # store 4
        self.market_proxy.add_quantity_to_store(self.store_id4, self.user_id4, self.product1.getProductId(), 100)
        self.market_proxy.add_quantity_to_store(self.store_id4, self.user_id4, self.product1.getProductId(), 170)
        self.market_proxy.add_quantity_to_store(self.store_id4, self.user_id4, self.product1.getProductId(), 30)
        self.market_proxy.add_quantity_to_store(self.store_id4, self.user_id4, self.product1.getProductId(), 20)
        self.market_proxy.add_quantity_to_store(self.store_id4, self.user_id4, self.product1.getProductId(), 10)
        # store 5
        self.market_proxy.add_quantity_to_store(self.store_id5, self.user_id5, self.product2.getProductId(), 100)
        self.market_proxy.add_quantity_to_store(self.store_id5, self.user_id5, self.product8.getProductId(), 170)
        self.market_proxy.add_quantity_to_store(self.store_id5, self.user_id5, self.product10.getProductId(), 65)
        self.market_proxy.add_quantity_to_store(self.store_id5, self.user_id5, self.product5.getProductId(), 45)
        self.market_proxy.add_quantity_to_store(self.store_id5, self.user_id5, self.product4.getProductId(), 35)
        # store 6
        self.market_proxy.add_quantity_to_store(self.store_id6, self.user_id1, self.product11.getProductId(), 43)
        self.market_proxy.add_quantity_to_store(self.store_id6, self.user_id1, self.product5.getProductId(), 225)
        self.market_proxy.add_quantity_to_store(self.store_id6, self.user_id1, self.product3.getProductId(), 543)
        self.market_proxy.add_quantity_to_store(self.store_id6, self.user_id1, self.product2.getProductId(), 24)
        self.market_proxy.add_quantity_to_store(self.store_id6, self.user_id1, self.product1.getProductId(), 543)
        # store 7
        self.market_proxy.add_quantity_to_store(self.store_id7, self.user_id2, self.product11.getProductId(), 43)
        self.market_proxy.add_quantity_to_store(self.store_id7, self.user_id2, self.product5.getProductId(), 225)
        self.market_proxy.add_quantity_to_store(self.store_id7, self.user_id2, self.product3.getProductId(), 543)
        self.market_proxy.add_quantity_to_store(self.store_id7, self.user_id2, self.product2.getProductId(), 24)
        self.market_proxy.add_quantity_to_store(self.store_id7, self.user_id2, self.product1.getProductId(), 543)
        # store 8
        self.market_proxy.add_quantity_to_store(self.store_id8, self.user_id3, self.product11.getProductId(), 14)
        self.market_proxy.add_quantity_to_store(self.store_id8, self.user_id3, self.product5.getProductId(), 15)
        self.market_proxy.add_quantity_to_store(self.store_id8, self.user_id3, self.product3.getProductId(), 34)
        self.market_proxy.add_quantity_to_store(self.store_id8, self.user_id3, self.product2.getProductId(), 54)
        self.market_proxy.add_quantity_to_store(self.store_id8, self.user_id3, self.product1.getProductId(), 634)


    def tearDown(self):
        self.market_proxy.removeStoreForGood(self.user_id3, self.store_id8)
        self.market_proxy.removeStoreForGood(self.user_id2, self.store_id7)
        self.market_proxy.removeStoreForGood(self.user_id1, self.store_id6)
        self.market_proxy.removeStoreForGood(self.user_id5, self.store_id5)
        self.market_proxy.removeStoreForGood(self.user_id4, self.store_id4)
        self.market_proxy.removeStoreForGood(self.user_id3, self.store_id3)
        self.market_proxy.removeStoreForGood(self.user_id2, self.store_id2)
        self.market_proxy.removeStoreForGood(self.user_id1, self.store_id1)
        self.user_proxy.removeMember("Manager", "user1")
        self.user_proxy.removeMember("Manager", "user2")
        self.user_proxy.removeMember("Manager", "user3")
        self.user_proxy.removeMember("Manager", "user4")
        self.user_proxy.removeMember("Manager", "user5")
        self.user_proxy.removeSystemManger_forTests("Manager")


    def test_add_to_cart_Login_Logout_positive1(self):
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id3, self.store_id1, self.product1.getProductId(),
                                                            10).getData())
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id3, self.store_id2, self.product3.getProductId(),
                                                            30).getData())
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id3, self.store_id2, self.product3.getProductId(),
                                                            30).getData())

        self.user_proxy.logout_member("user3")  # user logout!
        guest_id_2 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.login_member(guest_id_2, "user3", "123451")  # user login
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id3, self.store_id2, self.product3.getProductId(),
                                                            30).getData())
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id3, self.store_id2, self.product3.getProductId(),
                                                            30).getData())

        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id3, self.store_id2, self.product3.getProductId(),
                                                            30).isError())

        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id4, self.store_id2, self.product9.getProductId(),
                                                            30).getData())
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id4, self.store_id2, self.product9.getProductId(),
                                                            30).getData())


    def test_add_to_cart_negative1(self):
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id1, self.store_id1, -50, 10).isError())

    def test_add_to_cart_negative2(self):
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id1, 8, self.product1, 10).isError())

    def test_add_to_cart_negative3(self):
        self.assertTrue(self.user_proxy.add_product_to_cart(self.user_id1, self.store_id1, self.product1, 2500).isError())


if __name__ == '__main__':
    unittest.main()
