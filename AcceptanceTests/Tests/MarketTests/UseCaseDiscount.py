import sys
import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseDiscount(unittest.TestCase):
    # use-case 4.1.1
    @classmethod
    def setUpClass(cls):
        cls.proxy_market = MarketProxyBridge(MarketRealBridge())
        cls.proxy_user = UserProxyBridge(UserRealBridge())

        cls.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                              "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        cls.__guestId1 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser1", "1234", "0540000000", 123, [], "Israel", "Beer Sheva",
                                "Rager", 1,
                                "testBank")
        cls.user_id1 = cls.proxy_user.login_member(cls.__guestId1, "testUser1", "1234").getData().getUserID()

        cls.__guestId2 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser2", "12345", "0540000000", 123, [], "Israel", "Beer Sheva",
                                "Rager", 1,
                                "testBank")
        cls.user_id2 = cls.proxy_user.login_member(cls.__guestId2, "testUser2", "12345").getData().getUserID()

        cls.__guestId3 = cls.proxy_user.login_guest().getData().getUserID()
        cls.proxy_user.register("testUser3", "123456", "0540000000", 123, [], "Israel", "Beer Sheva",
                                "Rager", 1,
                                "testBank")
        cls.user_id3 = cls.proxy_user.login_member(cls.__guestId3, "testUser3", "123456").getData().getUserID()

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        cls.store_id1 = cls.proxy_user.open_store("testStore1", cls.user_id1, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()
        cls.store_id2 = cls.proxy_user.open_store("testStore2", cls.user_id2, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()
        cls.store_id3 = cls.proxy_user.open_store("testStore3", cls.user_id3, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        cls.product_id = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct1", 10,
                                                               "testCategory", 150, ["test"]).getData().getProductId()
        cls.product_id_2 = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct2", 100,
                                                                 "testCategory1", 150, ["test"]).getData().getProductId()
        cls.product_id_3 = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct3", 20,
                                                                 "testCategory", 150, ["test"]).getData().getProductId()

        cls.product_id_4 = cls.proxy_market.add_product_to_store(cls.store_id2, cls.user_id2, "testProduct4", 20,
                                                                 "testCategory1", 10, ["test"]).getData().getProductId()

        cls.product_id_5 = cls.proxy_market.add_product_to_store(cls.store_id3, cls.user_id3, "testProduct5", 45,
                                                                 "testCategory", 10, ["test"]).getData().getProductId()

        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id, 100)
        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id_2, 100)
        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id_3, 100)
        cls.proxy_market.add_quantity_to_store(cls.store_id2, cls.user_id2, cls.product_id_4, 150)
        cls.proxy_market.add_quantity_to_store(cls.store_id3, cls.user_id3, cls.product_id_5, 200)



    def test_armagdonCheckOfDiscounts(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData().getDiscountId() # 10 percent off to all store
        rId1 = self.proxy_market.addProductWeightRule(self.user_id1, self.store_id1, dId1, self.product_id, 100,
                                                      float('inf')).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityRule(self.user_id1, self.store_id1, dId1, "testCategory", 0,
                                                         1000).getData().getRuleId()

        rId3 = self.proxy_market.addStoreTotalAmountRule(self.user_id1, self.store_id1, dId1,0,
                                                         1500).getData().getRuleId()
        rId4 = self.proxy_market.addStoreTotalAmountRule(self.user_id1, self.store_id1, dId1, 0,
                                                         500).getData().getRuleId()

       # rId5 = self.proxy_market.addStoreQuantityRule(self.user_id1, self.store_id1, dId1, 0,
        #                                                 1).getData().getRuleId()
        #rId6 = self.proxy_market.addCategoryWeightRule(self.user_id1, self.store_id1, dId1,"testCategory" , 500,
         #                                                1000).getData().getRuleId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10) # 100 - 10
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10) # 1000 - 100
        first_rule =self.proxy_market.addCompositeRuleDiscountAnd(self.user_id1, self.store_id1, dId1, rId1, rId2).getData().getRuleId()
        second_rule = self.proxy_market.addCompositeRuleDiscountOr(self.user_id1, self.store_id1, dId1, rId3, rId4).getData().getRuleId()
        # third_rule = self.proxy_market.addCompositeRuleDiscountOr(self.user_id1, self.store_id1, dId1, rId5, rId6)
        fourt_rule = self.proxy_market.addCompositeRuleDiscountAnd(self.user_id1, self.store_id1, dId1, first_rule, second_rule)
        # self.proxy_market.addCompositeRuleDiscountAnd(self.user_id1, self.store_id1, dId1, third_rule, fourt_rule)
        # self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)
        self.assertEqual(990, userTransaction.getData().getTotalAmount())



if __name__ == '__main__':
    unittest.main()
