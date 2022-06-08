import sys
import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseDiscount(unittest.TestCase):
    # use-case 4.2

    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign system manager
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "Manager", "1234")
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser1", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                "Rager", 1, 0)
        self.user_id1 = self.proxy_user.login_member(self.__guestId1, "testUser1", "1234").getData().getUserID()

        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser2", "12345", "0540000000", 123, 1,  "Israel", "Beer Sheva",
                                "Rager", 1, 0)
        self.user_id2 = self.proxy_user.login_member(self.__guestId2, "testUser2", "12345").getData().getUserID()

        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser3", "123456", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                "Rager", 1, 0)
        self.user_id3 = self.proxy_user.login_member(self.__guestId3, "testUser3", "123456").getData().getUserID()

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id1 = self.proxy_user.open_store("testStore1", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()
        self.store_id2 = self.proxy_user.open_store("testStore2", self.user_id2, 123, 1, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()
        self.store_id3 = self.proxy_user.open_store("testStore3", self.user_id3, 123, 1, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        self.product_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
                                                               "testCategory", 150, ["test"]).getData().getProductId()
        self.product_id_2 = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct2", 100,
                                                                 "testCategory1", 150,
                                                                 ["test"]).getData().getProductId()
        self.product_id_3 = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct3", 20,
                                                                 "testCategory", 150, ["test"]).getData().getProductId()

        self.product_id_4 = self.proxy_market.add_product_to_store(self.store_id2, self.user_id2, "testProduct4", 20,
                                                                 "testCategory1", 150,
                                                                 ["test"]).getData().getProductId()

        self.product_id_5 = self.proxy_market.add_product_to_store(self.store_id3, self.user_id3, "testProduct5", 45,
                                                                 "testCategory", 10, ["test"]).getData().getProductId()

        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id, 100)
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id_2, 100)
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id_3, 100)
        self.proxy_market.add_quantity_to_store(self.store_id2, self.user_id2, self.product_id_4, 150)
        self.proxy_market.add_quantity_to_store(self.store_id3, self.user_id3, self.product_id_5, 200)

    def tearDown(self) -> None:
        self.proxy_user.exit_system(self.admin_id)
        self.proxy_user.exit_system(self.__guestId1)
        self.proxy_user.exit_system(self.__guestId2)
        self.proxy_user.exit_system(self.__guestId3)


        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id1)
        self.proxy_market.removeStoreForGood(self.user_id2, self.store_id2)
        self.proxy_market.removeStoreForGood(self.user_id3, self.store_id3)
        self.proxy_user.removeMember("Manager", "testUser1")
        self.proxy_user.removeMember("Manager", "testUser2")
        self.proxy_user.removeMember("Manager", "testUser3")
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_armagdonCheckOfDiscounts(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1,
                                                         0.1).getData().getDiscountId()  # 10 percent off to all store
        rId1 = self.proxy_market.addProductWeightDiscountRule(self.user_id1, self.store_id1, dId1, self.product_id, 100,
                                                              100000).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityDiscountRule(self.user_id1, self.store_id1, dId1, "testCategory", 0,
                                                                 1000).getData().getRuleId()

        rId3 = self.proxy_market.addStoreTotalAmountDiscountRule(self.user_id1, self.store_id1, dId1, 0,
                                                                 1500).getData().getRuleId()
        rId4 = self.proxy_market.addStoreTotalAmountDiscountRule(self.user_id1, self.store_id1, dId1, 0,
                                                                 500).getData().getRuleId()

        rId5 = self.proxy_market.addStoreQuantityDiscountRule(self.user_id1, self.store_id1, dId1, 0,
                                                              1).getData().getRuleId()
        rId6 = self.proxy_market.addCategoryWeightDiscountRule(self.user_id1, self.store_id1, dId1, "testCategory", 0,
                                                               100000).getData().getRuleId()
        # --------------------------------------------------

        dId2 = self.proxy_market.addSimpleDiscount_Product(self.user_id2, self.store_id2,
                                                           self.product_id_4,
                                                           0.1).getData().getDiscountId()  # 10 percent off to all store

        rId2_1 = self.proxy_market.addProductWeightDiscountRule(self.user_id2, self.store_id2, dId2, self.product_id_4,
                                                                0, 100000).getData().getRuleId()
        rId2_2 = self.proxy_market.addCategoryQuantityDiscountRule(self.user_id2, self.store_id2, dId2, "testCategory1",
                                                                   0,
                                                                   10000).getData().getRuleId()

        rId2_3 = self.proxy_market.addStoreTotalAmountDiscountRule(self.user_id2, self.store_id2, dId2, 0,
                                                                   10000).getData().getRuleId()
        rId2_4 = self.proxy_market.addStoreTotalAmountDiscountRule(self.user_id2, self.store_id2, dId2, 0,
                                                                   500).getData().getRuleId()

        rId2_5 = self.proxy_market.addStoreQuantityDiscountRule(self.user_id2, self.store_id2, dId2, 0,
                                                                1000).getData().getRuleId()
        rId2_6 = self.proxy_market.addCategoryWeightDiscountRule(self.user_id2, self.store_id2, dId2, "testCategory1",
                                                                 0,
                                                                 100000).getData().getRuleId()

        # --------------------------------------------------------------

        dId3 = self.proxy_market.addSimpleDiscount_Category(self.user_id3, self.store_id3,
                                                            "testCategory",
                                                            0.1).getData().getDiscountId()  # 10 percent off to all store

        rId3_1 = self.proxy_market.addProductWeightDiscountRule(self.user_id3, self.store_id3, dId3, self.product_id_5,
                                                                1000, 100000).getData().getRuleId()
        rId3_2 = self.proxy_market.addCategoryQuantityDiscountRule(self.user_id3, self.store_id3, dId3, "testCategory",
                                                                   0,
                                                                   10000).getData().getRuleId()

        rId3_3 = self.proxy_market.addStoreTotalAmountDiscountRule(self.user_id3, self.store_id3, dId3, 0,
                                                                   10000).getData().getRuleId()
        rId3_4 = self.proxy_market.addStoreTotalAmountDiscountRule(self.user_id3, self.store_id3, dId3, 0,
                                                                   500).getData().getRuleId()

        rId3_5 = self.proxy_market.addStoreQuantityDiscountRule(self.user_id3, self.store_id3, dId3, 0,
                                                                1000).getData().getRuleId()
        rId3_6 = self.proxy_market.addCategoryWeightDiscountRule(self.user_id3, self.store_id3, dId3, "testCategory1",
                                                                 0,
                                                                 100000).getData().getRuleId()

        first_rule_3 = self.proxy_market.addCompositeRuleDiscountOr(self.user_id3, self.store_id3, dId3, rId3_1,
                                                                    rId3_2).getData().getRuleId()
        second_rule_3 = self.proxy_market.addCompositeRuleDiscountOr(self.user_id3, self.store_id3, dId3, rId3_3,
                                                                     rId3_4).getData().getRuleId()
        third_rule_3 = self.proxy_market.addCompositeRuleDiscountAnd(self.user_id3, self.store_id3, dId3, rId3_5,
                                                                     rId3_6).getData().getRuleId()
        fourt_rule_3 = self.proxy_market.addCompositeRuleDiscountOr(self.user_id3, self.store_id3, dId3, first_rule_3,
                                                                    second_rule_3).getData().getRuleId()
        self.proxy_market.addCompositeRuleDiscountOr(self.user_id3, self.store_id3, dId3, third_rule_3,
                                                                    fourt_rule_3).getData().getRuleId()

        # ----------------------------------------------------

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)  # 100 - 10
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)  # 1000 - 100
        self.proxy_user.logout_member("testUser1")
        guestId = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(guestId, "testUser1", "1234")
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id2, self.product_id_4, 10)  # 100 - 10
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id3, self.product_id_5, 10)  # 100 - 10
        self.proxy_user.exit_system(guestId)


        first_rule_2 = self.proxy_market.addCompositeRuleDiscountAnd(self.user_id2, self.store_id2, dId2, rId2_1,
                                                                     rId2_2).getData().getRuleId()
        second_rule_2 = self.proxy_market.addCompositeRuleDiscountOr(self.user_id2, self.store_id2, dId2, rId2_3,
                                                                     rId2_4).getData().getRuleId()
        third_rule_2 = self.proxy_market.addCompositeRuleDiscountOr(self.user_id2, self.store_id2, dId2, rId2_5,
                                                                    rId2_6).getData().getRuleId()
        fourt_rule_2 = self.proxy_market.addCompositeRuleDiscountAnd(self.user_id2, self.store_id2, dId2, first_rule_2,
                                                                     second_rule_2).getData().getRuleId()
        self.proxy_market.addCompositeRuleDiscountAnd(self.user_id2, self.store_id2, dId2, third_rule_2,
                                                                     fourt_rule_2).getData().getRuleId()

        first_rule = self.proxy_market.addCompositeRuleDiscountAnd(self.user_id1, self.store_id1, dId1, rId1,
                                                                   rId2).getData().getRuleId()
        second_rule = self.proxy_market.addCompositeRuleDiscountOr(self.user_id1, self.store_id1, dId1, rId3,
                                                                   rId4).getData().getRuleId()
        third_rule = self.proxy_market.addCompositeRuleDiscountOr(self.user_id1, self.store_id1, dId1, rId5,
                                                                  rId6).getData().getRuleId()
        fourt_rule = self.proxy_market.addCompositeRuleDiscountAnd(self.user_id1, self.store_id1, dId1, first_rule,
                                                                   second_rule).getData().getRuleId()
        self.proxy_market.addCompositeRuleDiscountAnd(self.user_id1, self.store_id1, dId1, third_rule,
                                                                   fourt_rule).getData().getRuleId()

        dId4 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory",
                                                            0.3).getData().getDiscountId()  # 10 percent off to all store
        dId5 = self.proxy_market.addSimpleDiscount_Product(self.user_id2, self.store_id2, self.product_id_4,
                                                           0.05).getData().getDiscountId()  # 10 percent off to all store
        dId6 = self.proxy_market.addSimpleDiscount_Product(self.user_id3, self.store_id3, self.product_id_5,
                                                           0.3).getData().getDiscountId()  # 10 percent off to all store

        self.proxy_market.addConditionDiscountXor(self.user_id1, self.store_id1, dId1, dId4, 1)
        self.proxy_market.addConditionDiscountMax(self.user_id2, self.store_id2, dId2, dId5)
        self.proxy_market.addConditionDiscountAdd(self.user_id3, self.store_id3, dId3, dId6)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Kfir", "123", "123")
        if userTransaction.isError():
            print(userTransaction.getError())
        self.assertEqual(1440, userTransaction.getData().getTotalAmount())


if __name__ == '__main__':
    unittest.main()
