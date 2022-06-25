import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn

class UseCaseGetCartNEdit(unittest.TestCase):
    # use-case 2.8
    # get_cart functions has all products of a user from all the stores
    # also check changes in cart are working!
    # Proxies initialized
    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):
        print("set-up")
        # assign system manager & login system manager
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1).getData()
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "Manager", "1234")
        # create 5 users
        self.guest_id1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser1", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.guest_id2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.guest_id3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.guest_id4 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser4", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)
        self.guest_id5 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser5", "1234", "0540000000", 123, 5, "Israel", "Beer Sheva", "Rager", 1, 1)

        # 5 users log-in
        self.user_id1 = self.proxy_user.login_member(self.guest_id1, "testUser1", "1234").getData().getUserID()
        self.user_id2 = self.proxy_user.login_member(self.guest_id2, "testUser2", "1234").getData().getUserID()
        self.user_id3 = self.proxy_user.login_member(self.guest_id3, "testUser3", "1234").getData().getUserID()
        self.user_id4 = self.proxy_user.login_member(self.guest_id4, "testUser4", "1234").getData().getUserID()
        self.user_id5 = self.proxy_user.login_member(self.guest_id5, "testUser5", "1234").getData().getUserID()

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

    def tearDown(self):
        print("tear-down")
        # delete stores
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id1)
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id2)
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id3)
        # delete users
        self.proxy_user.removeMember("Manager", "testUser1")
        self.proxy_user.removeMember("Manager", "testUser2")
        self.proxy_user.removeMember("Manager", "testUser3")
        self.proxy_user.removeMember("Manager", "testUser4")
        self.proxy_user.removeMember("Manager", "testUser5")
        # remove system manager
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_cart_info_positive_simple(self):
        print("test_cart_info_positive_simple")
        bags = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()
        self.assertEqual(len(bags), 0, "There should be no bags!")
        # add product to user2's cart
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id1, self.p1_id, 1)
        bags = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()
        prods = list(bags.values())[0].getAllProducts()
        # user2 should have one bag (from one store)
        # user2 should have one product in the bag
        self.assertEqual(len(bags), 1, "There should only be one one bag.")
        self.assertEqual(len(prods), 1, "There should only be one product in the bag.")
        for prod in prods:
            self.assertEqual(prod.getProductId(), self.p1_id, "The product in the bag should be product1.")

        # teardown stuff - remove the prod from the cart
        self.proxy_user.remove_prod_from_cart(self.user_id2, self.store_id1, self.p1_id)

    def test_cart_info_positive_sequence_complex(self):
        print("test_cart_info_positive_sequence_complex")
        bags = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()
        self.assertEqual(len(bags), 0, "There should be no bags!")
        # add products to cart
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id1, self.p1_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id1, self.p2_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id2, self.p3_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id2, self.p4_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id3, self.p5_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id2, self.store_id3, self.p6_id, 10)
        # get all the bags in the cart of user2
        bags = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()
        self.assertEqual(len(bags), 3, "There 3 different bags from 3 different stores.")
        # get all the products in the bags
        prods_all_bags = [list(bags.values())[0].getAllProducts(), list(bags.values())[1].getAllProducts(), list(bags.values())[2].getAllProducts()]
        # 2 products in each bag
        for bag in prods_all_bags:
            self.assertEqual(len(bag), 2, "There should be 2 prods in each bag")

        # remove product1 from cart
        self.proxy_user.remove_prod_from_cart(self.user_id2, self.store_id1, self.p1_id)
        prods1 = list(self.proxy_user.get_cart(self.user_id2).getData().getAllBags().values())[0].getAllProducts()
        self.assertEqual(len(prods1), 1, "We removed product1 from cart!")
        self.proxy_user.update_prod_from_cart(self.user_id2, self.store_id2, self.p3_id, 30)
        prods2 = list(self.proxy_user.get_cart(self.user_id2).getData().getAllBags().values())[1].getAllProducts()
        self.assertEqual(list(prods2.values())[0], 40, "We added 30 more pieces to product3!")

        # remove the rest of the products
        self.proxy_user.remove_prod_from_cart(self.user_id2, self.store_id1, self.p2_id)
        self.proxy_user.remove_prod_from_cart(self.user_id2, self.store_id2, self.p3_id)
        self.proxy_user.remove_prod_from_cart(self.user_id2, self.store_id2, self.p4_id)
        self.proxy_user.remove_prod_from_cart(self.user_id2, self.store_id3, self.p5_id)
        self.proxy_user.remove_prod_from_cart(self.user_id2, self.store_id3, self.p6_id)
        bags = self.proxy_user.get_cart(self.user_id2).getData().getAllBags()
        self.assertFalse(bags, "We removed all the products, bags should be empty.")

    def test_cart_info_threads(self):
        print("test_cart_info_threads")
        # only one buys each time!
        t = []
        # one buys product1
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args =(self.user_id3, self.store_id1, self.p1_id, 100)))
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args = (self.user_id4, self.store_id1, self.p1_id, 100)))
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args =(self.user_id5, self.store_id1, self.p1_id, 100)))
        t.append(ThreadWithReturn(
            target=self.proxy_user.add_product_to_cart, args = (self.user_id2, self.store_id1, self.p1_id, 100)))

        # one buys product3
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args = (self.user_id3, self.store_id2, self.p3_id, 100)))
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args = (self.user_id4, self.store_id2, self.p3_id, 100)))
        t.append(ThreadWithReturn(
            target=self.proxy_user.add_product_to_cart, args = (self.user_id5, self.store_id2, self.p3_id, 100)))
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args =(self.user_id2, self.store_id2, self.p3_id, 100)))

        # one buys product 5
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args=(self.user_id3, self.store_id3, self.p5_id, 100)))
        t.append(ThreadWithReturn(
            target=self.proxy_user.add_product_to_cart, args = (self.user_id4, self.store_id3, self.p5_id, 90)))
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args= (self.user_id5, self.store_id3, self.p5_id, 90)))
        t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart, args = (self.user_id2, self.store_id3, self.p5_id, 90)))

        for th in t:
            th.start()

        for th in t:
            th.join()

        bags= [self.proxy_user.get_cart(self.user_id2).getData().getAllBags(),
               self.proxy_user.get_cart(self.user_id3).getData().getAllBags(),
               self.proxy_user.get_cart(self.user_id4).getData().getAllBags(),
               self.proxy_user.get_cart(self.user_id5).getData().getAllBags()]

        bags_len = 0
        for bag in bags:
            bags_len += len(bag)
        self.assertEqual(bags_len, 3, "only 3 should succeed adding to cart.")

    # def test_add_n_remove_products_from_cart_threads(self):
    #     t = []
    #     for i in range(200):
    #         t.append(ThreadWithReturn(target=self.proxy_user.add_product_to_cart,
    #                               args=(self.user_id3, self.store_id1, self.p1_id, 1)))
    #     for th in t:
    #         th.start()
    #     success = 0
    #     fail = 0
    #     for th in t:
    #         if th.join().getData():
    #             success += 1
    #         else:
    #             fail += 1
    #     self.assertEqual(success,fail, "100 products in store - 100 should succeed to add and 100 should fail!")
    #
    #     t.clear()
    #     t.append(ThreadWithReturn(target=self.proxy_user.remove_prod_from_cart,
    #                               args=(self.user_id3, self.store_id1, self.p1_id)))
    #     t.append(ThreadWithReturn(target=self.proxy_user.remove_prod_from_cart,
    #                               args=(self.user_id3, self.store_id1, self.p1_id)))
    #     t[0].start()
    #     t[1].start()
    #     ans1 = t[0].join()
    #     ans2 = t[1].join()
    #     print(ans1.getData())
    #     print(ans2.getData())
    #     self.assertTrue(ans1.isError() or ans2.isError(), "you can only delete product from cart once!")

if __name__ == '__main__':
    unittest.main()
