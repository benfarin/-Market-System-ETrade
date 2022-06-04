import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseSaveProductToCart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.market_proxy = MarketProxyBridge(MarketRealBridge())
        cls.user_proxy = UserProxyBridge(UserRealBridge())
        cls.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                              "Ben Gurion", 1, 1)
        # --------------------------users register ------------------------------------
        cls.__guestId1 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user1", "1234", "053643643", "500", "20", "Israel", "Beer Sheva",
                                "Ben Gurion", 0, 0)
        cls.__guestId2 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user2", "12345", "0500000000", "505", "21", "Israel", "Tel aviv",
                                "Ben Gurion", 0, 0)
        cls.__guestId3 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user3", "123451", "05325235", "506", "22", "Israel", "Tel aviv",
                                "Ben Gurion", 0, 0)
        cls.__guestId4 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user4", "123452", "0503643342", "402", "2124", "Israel", "Tel aviv",
                                "Ben Gurion", 0, 0)
        cls.__guestId5 = cls.user_proxy.login_guest().getData().getUserID()
        cls.user_proxy.register("user5", "123456", "05043523523", "505", "21", "Israel", "ashdod",
                                "Ben Gurion", 0, 0)

        # ----------------------------user login --------------------------------------
        cls.user_id1 = cls.user_proxy.login_member(cls.__guestId1, "user1", "1234").getData().getUserID()
        cls.user_id2 = cls.user_proxy.login_member(cls.__guestId2, "user2", "12345").getData().getUserID()
        cls.user_id3 = cls.user_proxy.login_member(cls.__guestId3, "user3", "123451").getData().getUserID()
        cls.user_id4 = cls.user_proxy.login_member(cls.__guestId4, "user4", "123452").getData().getUserID()
        cls.user_id5 = cls.user_proxy.login_member(cls.__guestId5, "user5", "123456").getData().getUserID()

        # ------------------------------------open stores-----------------------------------------------------
        cls.store_id1 = cls.user_proxy.open_store("store1", cls.user_id1, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, "000000").getData().getStoreId()
        cls.store_id2 = cls.user_proxy.open_store("store2", cls.user_id2, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, "000000").getData().getStoreId()
        cls.store_id3 = cls.user_proxy.open_store("store3", cls.user_id3, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, "000000").getData().getStoreId()
        cls.store_id4 = cls.user_proxy.open_store("store4", cls.user_id4, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, "000000").getData().getStoreId()
        cls.store_id5 = cls.user_proxy.open_store("store5", cls.user_id5, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, "000000").getData().getStoreId()

        cls.store_id6 = cls.user_proxy.open_store("store6", cls.user_id1, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, "000000").getData().getStoreId()
        cls.store_id7 = cls.user_proxy.open_store("store7", cls.user_id2, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, "000000").getData().getStoreId()
        cls.store_id8 = cls.user_proxy.open_store("store8", cls.user_id3, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                                  0, "000000").getData().getStoreId()

        # ------------------------------------------- products ----------------------------------------------------
        cls.product1 = cls.market_proxy.add_product_to_store(cls.store_id1, cls.user_id1, "Milk 5%", 500,
                                                             "Milky", 10, ["Milk", "Tara", "5%"]).getData()
        cls.product2 = cls.market_proxy.add_product_to_store(cls.store_id1, cls.user_id1, "Chocolate", 500,
                                                             "Milky", 15, ["Test1", "Test2"]).getData()

        cls.product3 = cls.market_proxy.add_product_to_store(cls.store_id2, cls.user_id2, "Product", 500,
                                                             "Category", 7, ["Test1", "Test2"]).getData()
        cls.product4 = cls.market_proxy.add_product_to_store(cls.store_id2, cls.user_id2, "Product", 500,
                                                             "Category", 9, ["Test1", "Test2"]).getData()

        cls.product5 = cls.market_proxy.add_product_to_store(cls.store_id3, cls.user_id3, "Product", 500,
                                                             "Category", 30, ["Test1", "Test2"]).getData()
        cls.product6 = cls.market_proxy.add_product_to_store(cls.store_id3, cls.user_id3, "Product", 500,
                                                             "Category", 1, ["Test1", "Test2"]).getData()

        cls.product7 = cls.market_proxy.add_product_to_store(cls.store_id4, cls.user_id4, "Product", 500,
                                                             "Category", 8, ["Test1", "Test2"]).getData()
        cls.product8 = cls.market_proxy.add_product_to_store(cls.store_id4, cls.user_id4, "Product", 500,
                                                             "Category", 10, ["Test1", "Test2"]).getData()

        cls.product9 = cls.market_proxy.add_product_to_store(cls.store_id2, cls.user_id2, "Product", 500,
                                                             "Category", 10, ["Test1", "Test2"]).getData()
        cls.product10 = cls.market_proxy.add_product_to_store(cls.store_id5, cls.user_id5, "Product", 500,
                                                              "Category", 10, ["Test1", "Test2"]).getData()

        cls.product11 = cls.market_proxy.add_product_to_store(cls.store_id6, cls.user_id1, "Product", 500,
                                                              "Category", 12, ["Test1", "Test2"]).getData()
        cls.product12 = cls.market_proxy.add_product_to_store(cls.store_id6, cls.user_id1, "Product", 500,
                                                              "Category", 18, ["Test1", "Test2"]).getData()

        cls.product13 = cls.market_proxy.add_product_to_store(cls.store_id7, cls.user_id2, "Product", 500,
                                                              "Category", 20, ["Test1", "Test2"]).getData()
        cls.product14 = cls.market_proxy.add_product_to_store(cls.store_id7, cls.user_id2, "Product", 500,
                                                              "Category", 22, ["Test1", "Test2"]).getData()

        cls.product15 = cls.market_proxy.add_product_to_store(cls.store_id8, cls.user_id3, "Product", 500,
                                                              "Category", 24, ["Test1", "Test2"]).getData()
        cls.product16 = cls.market_proxy.add_product_to_store(cls.store_id8, cls.user_id3, "Product", 500,
                                                              "Category", 5, ["Test1", "Test2"]).getData()

        # ----------------------------------------- add quantity to stores ----------------------------------------

        # store 1
        cls.market_proxy.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product1.getProductId(), 100)
        cls.market_proxy.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product2.getProductId(), 50)
        cls.market_proxy.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product3.getProductId(), 45)
        cls.market_proxy.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product4.getProductId(), 80)
        cls.market_proxy.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product5.getProductId(), 70)
        # store 2
        cls.market_proxy.add_quantity_to_store(cls.store_id2, cls.user_id2, cls.product3.getProductId(), 120)
        cls.market_proxy.add_quantity_to_store(cls.store_id2, cls.user_id2, cls.product9.getProductId(), 100)
        cls.market_proxy.add_quantity_to_store(cls.store_id2, cls.user_id2, cls.product7.getProductId(), 75)
        cls.market_proxy.add_quantity_to_store(cls.store_id2, cls.user_id2, cls.product8.getProductId(), 110)
        cls.market_proxy.add_quantity_to_store(cls.store_id2, cls.user_id2, cls.product1.getProductId(), 90)
        # store 3
        cls.market_proxy.add_quantity_to_store(cls.store_id3, cls.user_id3, cls.product1.getProductId(), 140)
        cls.market_proxy.add_quantity_to_store(cls.store_id3, cls.user_id3, cls.product1.getProductId(), 120)
        cls.market_proxy.add_quantity_to_store(cls.store_id3, cls.user_id3, cls.product1.getProductId(), 170)
        cls.market_proxy.add_quantity_to_store(cls.store_id3, cls.user_id3, cls.product1.getProductId(), 170)
        # store 4
        cls.market_proxy.add_quantity_to_store(cls.store_id4, cls.user_id4, cls.product1.getProductId(), 100)
        cls.market_proxy.add_quantity_to_store(cls.store_id4, cls.user_id4, cls.product1.getProductId(), 170)
        cls.market_proxy.add_quantity_to_store(cls.store_id4, cls.user_id4, cls.product1.getProductId(), 30)
        cls.market_proxy.add_quantity_to_store(cls.store_id4, cls.user_id4, cls.product1.getProductId(), 20)
        cls.market_proxy.add_quantity_to_store(cls.store_id4, cls.user_id4, cls.product1.getProductId(), 10)
        # store 5
        cls.market_proxy.add_quantity_to_store(cls.store_id5, cls.user_id5, cls.product2.getProductId(), 100)
        cls.market_proxy.add_quantity_to_store(cls.store_id5, cls.user_id5, cls.product8.getProductId(), 170)
        cls.market_proxy.add_quantity_to_store(cls.store_id5, cls.user_id5, cls.product10.getProductId(), 65)
        cls.market_proxy.add_quantity_to_store(cls.store_id5, cls.user_id5, cls.product5.getProductId(), 45)
        cls.market_proxy.add_quantity_to_store(cls.store_id5, cls.user_id5, cls.product4.getProductId(), 35)
        # store 6
        cls.market_proxy.add_quantity_to_store(cls.store_id6, cls.user_id1, cls.product11.getProductId(), 43)
        cls.market_proxy.add_quantity_to_store(cls.store_id6, cls.user_id1, cls.product5.getProductId(), 225)
        cls.market_proxy.add_quantity_to_store(cls.store_id6, cls.user_id1, cls.product3.getProductId(), 543)
        cls.market_proxy.add_quantity_to_store(cls.store_id6, cls.user_id1, cls.product2.getProductId(), 24)
        cls.market_proxy.add_quantity_to_store(cls.store_id6, cls.user_id1, cls.product1.getProductId(), 543)
        # store 7
        cls.market_proxy.add_quantity_to_store(cls.store_id7, cls.user_id2, cls.product11.getProductId(), 43)
        cls.market_proxy.add_quantity_to_store(cls.store_id7, cls.user_id2, cls.product5.getProductId(), 225)
        cls.market_proxy.add_quantity_to_store(cls.store_id7, cls.user_id2, cls.product3.getProductId(), 543)
        cls.market_proxy.add_quantity_to_store(cls.store_id7, cls.user_id2, cls.product2.getProductId(), 24)
        cls.market_proxy.add_quantity_to_store(cls.store_id7, cls.user_id2, cls.product1.getProductId(), 543)
        # store 8
        cls.market_proxy.add_quantity_to_store(cls.store_id8, cls.user_id3, cls.product11.getProductId(), 14)
        cls.market_proxy.add_quantity_to_store(cls.store_id8, cls.user_id3, cls.product5.getProductId(), 15)
        cls.market_proxy.add_quantity_to_store(cls.store_id8, cls.user_id3, cls.product3.getProductId(), 34)
        cls.market_proxy.add_quantity_to_store(cls.store_id8, cls.user_id3, cls.product2.getProductId(), 54)
        cls.market_proxy.add_quantity_to_store(cls.store_id8, cls.user_id3, cls.product1.getProductId(), 634)

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
