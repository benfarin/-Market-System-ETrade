import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UseCaseGetCartNEdit(unittest.TestCase):
    # usecase 2.8
    # get_cart functions has all products of a user from all the stores
    # also check changes in cart are working!

    @classmethod
    def setUpClass(cls) -> None:
        print("NEVER CALLED")

    def setUp(self) -> None:
        # Proxies initialized
        self.proxy_market = MarketProxyBridge(MarketRealBridge())
        self.proxy_user = UserProxyBridge(UserRealBridge())

        # assign system manager
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)

        # create 5 users
        guest_id1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser1", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)
        guest_id2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)
        guest_id3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)
        guest_id4 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser4", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)
        guest_id5 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser5", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)

        # 5 users log-in
        self.user_id1 = self.proxy_user.login_member(guest_id1, "testUser1", "1234").getData().getUserID()
        self.user_id2 = self.proxy_user.login_member(guest_id2, "testUser2", "1234").getData().getUserID()
        self.user_id3 = self.proxy_user.login_member(guest_id3, "testUser3", "1234").getData().getUserID()
        self.user_id4 = self.proxy_user.login_member(guest_id4, "testUser4", "1234").getData().getUserID()
        self.user_id5 = self.proxy_user.login_member(guest_id5, "testUser5", "1234").getData().getUserID()

        # Create 3 stores
        self.store_id1 = self.proxy_user.open_store("fruits_store", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()
        self.store_id2 = self.proxy_user.open_store("cloths_store", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()
        self.store_id3 = self.proxy_user.open_store("game_store", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 00000).getData().getStoreId()

        # Add products to the stores
        self.p1_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "apple", 10, "red_fruit", 15,
                                                            ["red"]).getData().getProductId()
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.p1_id, 100)

        self.p2_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "banana", 100,
                                                            "yellow_fruit", 10, ["yellow"]).getData().getProductId()
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.p2_id, 100)

        self.p3_id = self.proxy_market.add_product_to_store(self.store_id2, self.user_id1, "shirt", 100,
                                                            "basic_clothing", 10, ["basic"]).getData().getProductId()
        self.proxy_market.add_quantity_to_store(self.store_id2, self.user_id1, self.p3_id, 100)

        self.p4_id = self.proxy_market.add_product_to_store(self.store_id2, self.user_id1, "pants", 100,
                                                            "basic_clothing", 10, ["basic"]).getData().getProductId()
        self.proxy_market.add_quantity_to_store(self.store_id2, self.user_id1, self.p4_id, 100)

        self.p5_id = self.proxy_market.add_product_to_store(self.store_id3, self.user_id1, "poker", 100, "gambling", 10,
                                                            ["gambling"]).getData().getProductId()
        self.proxy_market.add_quantity_to_store(self.store_id3, self.user_id1, self.p5_id, 100)

        self.p6_id = self.proxy_market.add_product_to_store(self.store_id3, self.user_id1, "monopoly", 100,
                                                            "board_games", 10, ["board"]).getData().getProductId()
        self.proxy_market.add_quantity_to_store(self.store_id3, self.user_id1, self.p6_id, 100)

    def test_cart_info_positive_simple(self):
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id1, self.p1_id, 1)
        bags = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()
        prods = bags[0].getAllProducts()
        self.assertEqual(len(bags), 1, "There should only be one one bag.")
        self.assertEqual(len(prods), 1, "There should only be one product in the bag.")
        for prod in prods:
            self.assertEqual(prod.getProductId(), self.p1_id, "The product in the bag should be product1.")

    def test_cart_info_positive_sequence_complex(self):
        # add products to cart
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id1, self.p1_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id1, self.p2_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id2, self.p3_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id2, self.p4_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id3, self.p5_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id3, self.p6_id, 10)
        # get all the bags in the cart
        bags = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()
        self.assertEqual(len(bags), 3, "There 3 different bags from 3 different stores.")
        # get all the products in the bags
        prods1 = bags[0].getAllProducts()
        prods2 = bags[1].getAllProducts()
        prods3 = bags[2].getAllProducts()
        self.assertEqual(len(prods1), 2)
        self.assertEqual(len(prods2), 2)
        self.assertEqual(len(prods3), 2)
        # remove product1 from cart
        self.proxy_user.remove_prod_from_cart(self.user_id2, self.store_id1, self.p1_id)
        prods1 = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()[0].getAllProducts()
        self.assertEqual(len(prods1), 1, "We removed product1 from cart!")
        self.proxy_user.update_prod_from_cart(self.user_id2, self.store_id2, self.p3_id, 30)
        prods2 = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()[1].getAllProducts()
        self.assertEqual(list(prods2.values())[0], 40, "We added 30 more pieces to product3!")

    def test_cart_info_threads(self):
        # user2 shouldn't succeed to buy
        t1 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args =(self.user_id3, self.store_id1, self.p1_id, 10))
        t2 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args = (self.user_id4, self.store_id1, self.p1_id, 10))
        t3 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args =(self.user_id5, self.store_id1, self.p1_id, 10))
        t4 = ThreadWithReturn(
            target=self.proxy_user.add_product_to_cart, args = (self.user_id2, self.store_id1, self.p1_id, 100))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        # user5 shouldn't succeed to buy
        t1 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args = (self.user_id3, self.store_id2, self.p3_id, 10))
        t2 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args = (self.user_id4, self.store_id2, self.p3_id, 10))
        t3 = ThreadWithReturn(
            target=self.proxy_user.add_product_to_cart, args = (self.user_id5, self.store_id2, self.p3_id, 100))
        t4 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args =(self.user_id2, self.store_id2, self.p3_id, 10))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        # user4 shouldn't succeed to buy
        t1 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args=(self.user_id3, self.store_id3, self.p5_id, 10))
        t2 = ThreadWithReturn(
            target=self.proxy_user.add_product_to_cart, args = (self.user_id4, self.store_id3, self.p5_id, 100))
        t3 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args= (self.user_id5, self.store_id3, self.p5_id, 10))
        t4 = ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args = (self.user_id2, self.store_id3, self.p5_id, 10))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        bags1 = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()
        bags2 = self.proxy_user.get_cart(self.user_id3).getData().getAllBags()
        bags3 = self.proxy_user.get_cart(self.user_id4).getData().getAllBags()
        bags4 = self.proxy_user.get_cart(self.user_id5).getData().getAllBags()

        # due to threads, the result isn't constants, need to modify!!!
        self.assertEqual(len(bags1), 2, "user2 bought from 2 different stores!")
        self.assertEqual(len(bags2), 3, "user3 bought from 3 different stores!")
        self.assertEqual(len(bags3), 2, "user4 bought from 2 different stores!")
        self.assertEqual(len(bags4), 2, "user5 bought from 2 different stores!")


if __name__ == '__main__':
    unittest.main()
