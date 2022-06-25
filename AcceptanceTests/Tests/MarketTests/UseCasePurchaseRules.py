import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from AcceptanceTests.Tests.ThreadWithReturn import ThreadWithReturn


class UseCasePurchaseRules(unittest.TestCase):
    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())

    def setUp(self):
        # assign system manager
        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        self.admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.admin_id, "Manager", "1234")
        # create 3 users
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.__guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Rotem", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                "Rager", 1, 0)
        self.proxy_user.register("Ori", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.proxy_user.register("Kfir", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        # login 3 users
        self.user_id1 = self.proxy_user.login_member(self.__guestId1, "Rotem", "1234").getData().getUserID()
        self.user_id2 = self.proxy_user.login_member(self.__guestId2, "Ori", "1234").getData().getUserID()
        self.user_id3 = self.proxy_user.login_member(self.__guestId3, "Kfir", "1234").getData().getUserID()

        # create 2 stores
        self.store_id1 = self.proxy_user.open_store("Rotem", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        self.store_id2 = self.proxy_user.open_store("Ori", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        # add to stores 4 products
        self.product_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
                                                               "testCategory", 20, ["test"]).getData().getProductId()
        self.product_id_2 = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct2", 100,
                                                                 "testCategory1", 17, ["test"]).getData().getProductId()
        self.product_id_3 = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct3", 20,
                                                                 "testCategory", 15, ["test"]).getData().getProductId()
        self.product_id_4 = self.proxy_market.add_product_to_store(self.store_id2, self.user_id1, "testProduct4", 10,
                                                                 "testCategory", 15, ["test"]).getData().getProductId()

        # add quantity of products to store
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id, 100)
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id_2, 100)
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id_3, 100)
        self.proxy_market.add_quantity_to_store(self.store_id2, self.user_id1, self.product_id_4, 100)

    def tearDown(self):
        # remove 2 stores
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id1)
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id2)
        # remove 3 users
        self.proxy_user.removeMember("Manager", "Rotem")
        self.proxy_user.removeMember("Manager", "Ori")
        self.proxy_user.removeMember("Manager", "Kfir")
        # remove system manager
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_addSimpleRuleStore(self):
        r_id = self.proxy_market.addStoreTotalAmountPurchaseRule(self.user_id1, self.store_id1,
                                                                 100, 2000).getData().getRuleId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")

        self.assertEqual(1100, userTransaction.getData().getTotalAmount())
        rulesInDiscountIds = [rule.getRuleId() for rule in
                              self.proxy_market.getAllSimplePurchaseRulesOfStore(self.user_id1,
                                                                                 self.store_id1).getData()]
        self.assertEqual(rulesInDiscountIds, [r_id])

    def test_addSimpleRuleStore_NotPassing(self):
        r_id = self.proxy_market.addStoreTotalAmountPurchaseRule(self.user_id1, self.store_id1,
                                                                 1500, 10000).getData().getRuleId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")

        self.assertEqual(0, userTransaction.getData().getTotalAmount())
        rulesInDiscountIds = [rule.getRuleId() for rule in
                              self.proxy_market.getAllSimplePurchaseRulesOfStore(self.user_id1,
                                                                                 self.store_id1).getData()]
        self.assertEqual(rulesInDiscountIds, [r_id])

    def test_addCondPurchaseRule_AND(self):
        rId1 = self.proxy_market.addProductWeightPurchaseRule(self.user_id1, self.store_id1, self.product_id, 300, 100000).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityPurchaseRule(self.user_id1, self.store_id1, "testCategory1", 0, 5).getData().getRuleId()
        r_id = self.proxy_market.addCompositeRulePurchaseAnd(self.user_id1, self.store_id1, rId1, rId2).getData().getRuleId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)  ### Price: 10 * 10 = 100, Weight: 10 * 20 = 200
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10) ### Price 10 * 100 = 1000
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")

        self.assertEqual(0, userTransaction.getData().getTotalAmount())
        rulesInDiscountIds = [rule.getRuleId() for rule in
                              self.proxy_market.getAllSimplePurchaseRulesOfStore(self.user_id1,
                                                                                 self.store_id1).getData()]
        self.assertEqual(rulesInDiscountIds, [])
        rulesInDiscountIds = [rule.getRuleId() for rule in
                              self.proxy_market.getAllCompositePurchaseRulesOfStore(self.user_id1,
                                                                                    self.store_id1).getData()]
        self.assertEqual(rulesInDiscountIds, [r_id])

    def test_addCondDiscountRule_OR(self):
        rId1 = self.proxy_market.addProductQuantityPurchaseRule(self.user_id1, self.store_id1, self.product_id, 5, 100000).getData().getRuleId()
        rId2 = self.proxy_market.addStoreQuantityPurchaseRule(self.user_id1, self.store_id1, 0, 30).getData().getRuleId()
        r_id = self.proxy_market.addCompositeRulePurchaseAnd(self.user_id1, self.store_id1, rId1, rId2).getData().getRuleId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")

        self.assertEqual(1100, userTransaction.getData().getTotalAmount())
        rulesInDiscountIds = [rule.getRuleId() for rule in
                              self.proxy_market.getAllSimplePurchaseRulesOfStore(self.user_id1,
                                                                                 self.store_id1).getData()]
        self.assertEqual(rulesInDiscountIds, [])
        rulesInDiscountIds = [rule.getRuleId() for rule in
                              self.proxy_market.getAllCompositePurchaseRulesOfStore(self.user_id1,
                                                                                    self.store_id1).getData()]
        self.assertEqual(rulesInDiscountIds, [r_id])

    def test_addCondDiscountRule_OR_AND_with_discount(self):   ######FAILING
        self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id1, self.product_id_2, 0.1).getData().getDiscountId()

        rId1 = self.proxy_market.addProductWeightPurchaseRule(self.user_id1, self.store_id1, self.product_id, 100, 100000).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityPurchaseRule(self.user_id1, self.store_id1, "testCategory", 0, 5).getData().getRuleId()
        rId3 = self.proxy_market.addStoreTotalAmountPurchaseRule(self.user_id1, self.store_id1, 5, 100000).getData().getRuleId()

        rOr_id = self.proxy_market.addCompositeRulePurchaseOr(self.user_id1, self.store_id1, rId1, rId2).getData().getRuleId()
        r_id = self.proxy_market.addCompositeRulePurchaseAnd(self.user_id1, self.store_id1, rId3, rOr_id).getData().getRuleId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")
        print(userTransaction)

        self.assertEqual(1000, userTransaction.getData().getTotalAmount())
        rulesInDiscountIds = [rule.getRuleId() for rule in
                              self.proxy_market.getAllSimplePurchaseRulesOfStore(self.user_id1,
                                                                                 self.store_id1).getData()]
        self.assertEqual(rulesInDiscountIds, [])
        rulesInDiscountIds = [rule.getRuleId() for rule in
                              self.proxy_market.getAllCompositePurchaseRulesOfStore(self.user_id1,
                                                                                    self.store_id1).getData()]
        self.assertEqual(rulesInDiscountIds, [r_id])


if __name__ == '__main__':
    unittest.main()
