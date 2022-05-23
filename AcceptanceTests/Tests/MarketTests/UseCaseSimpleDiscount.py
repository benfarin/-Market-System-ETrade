import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseSimpleDiscount(unittest.TestCase):
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

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        cls.store_id1 = cls.proxy_user.open_store("testStore1", cls.user_id1, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        cls.store_id2 = cls.proxy_user.open_store("testStore2", cls.user_id1, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        cls.product_id = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct1", 10,
                                                               "testCategory", 20, ["test"]).getData().getProductId()
        cls.product_id_2 = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct2", 100,
                                                                 "testCategory1", 17, ["test"]).getData().getProductId()
        cls.product_id_3 = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct3", 20,
                                                                 "testCategory", 15, ["test"]).getData().getProductId()
        cls.product_id_4 = cls.proxy_market.add_product_to_store(cls.store_id2, cls.user_id1, "testProduct4", 10,
                                                                 "testCategory", 15, ["test"]).getData().getProductId()

        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id, 100)
        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id_2, 100)
        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id_3, 100)
        cls.proxy_market.add_quantity_to_store(cls.store_id2, cls.user_id1, cls.product_id_4, 100)

    def test_addSimpleDiscountStore(self):
        self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(990, userTransaction.getData().getTotalAmount())

    def test_addSimpleDiscountCategory(self):
        self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory", 0.1).getData()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_3, 5)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1180, userTransaction.getData().getTotalAmount())

    def test_addSimpleDiscountProduct(self):
        self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id1, self.product_id_3, 0.1).getData()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_3, 5)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1190, userTransaction.getData().getTotalAmount())

    def test_addCoupleOfSimpleDiscount(self):
        self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory", 0.1)
        self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id1, self.product_id_3, 0.5)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_3, 5)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1150, userTransaction.getData().getTotalAmount())

    def test_addCoupleOfSimpleDiscountFromDiffrenceStores(self):
        self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory", 0.1)
        self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id2, self.product_id_4, 0.5)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id2, self.product_id_4, 10)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(140, userTransaction.getData().getTotalAmount())

    def test_addDiscountAdd(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData().getDiscountId()
        dId2 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory",
                                                            0.4).getData().getDiscountId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        self.proxy_market.addConditionDiscountAdd(self.user_id1, self.store_id1, dId1, dId2)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(950, userTransaction.getData().getTotalAmount())

    def test_addDiscountMax(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData().getDiscountId()
        dId2 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory",
                                                            0.4).getData().getDiscountId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        self.proxy_market.addConditionDiscountMax(self.user_id1, self.store_id1, dId1, dId2)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(990, userTransaction.getData().getTotalAmount())

    def test_addDiscountAddMax(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData().getDiscountId()
        dId2 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory1",
                                                            0.4).getData().getDiscountId()
        dId3 = self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id1, self.product_id,
                                                           0.1).getData().getDiscountId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)

        dId4 = self.proxy_market.addConditionDiscountMax(self.user_id1, self.store_id1, dId1,
                                                         dId2).getData().getDiscountId()
        self.proxy_market.addConditionDiscountAdd(self.user_id1, self.store_id1, dId3, dId4)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)
        self.assertEqual(690, userTransaction.getData().getTotalAmount())

    def test_addDiscountAddXor(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData().getDiscountId()
        dId2 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory1",
                                                            0.4).getData().getDiscountId()

        self.proxy_market.addStoreTotalAmountRule(self.user_id1, self.store_id1, dId1, 2000, 3000)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)

        self.proxy_market.addConditionDiscountXor(self.user_id1, self.store_id1, dId1, dId2, 1)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)
        self.assertEqual(700, userTransaction.getData().getTotalAmount())

    def test_removeDiscount(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData().getDiscountId()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)

        self.proxy_market.removeDiscount(self.user_id1, self.store_id1, dId1)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)
        self.assertEqual(1100, userTransaction.getData().getTotalAmount())

    def test_addSimpleDiscountRule_1(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData().getDiscountId()
        self.proxy_market.addStoreQuantityRule(self.user_id1, self.store_id1, dId1, 200, float('inf'))

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)
        self.assertEqual(1100, userTransaction.getData().getTotalAmount())

    def test_addSimpleDiscountRule_2(self):
        dId1 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, "testCategory", 0.1).getData().getDiscountId()
        self.proxy_market.addProductWeightRule(self.user_id1, self.store_id1, dId1, self.product_id, 900, 1000)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1100, userTransaction.getData().getTotalAmount())

    def test_addCondDiscountRule_AND(self):
        dId1 = self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id1, self.product_id_2, 0.1).getData().getDiscountId()
        rId1 = self.proxy_market.addProductWeightRule(self.user_id1, self.store_id1, dId1, self.product_id, 100, float('inf')).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityRule(self.user_id1, self.store_id1, dId1, "testCategory", 0, 5).getData().getRuleId()
        self.proxy_market.addCompositeRuleDiscountAnd(self.user_id1, self.store_id1, dId1, rId1, rId2)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1100, userTransaction.getData().getTotalAmount())

    def test_addCondDiscountRule_OR(self):
        dId1 = self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id1, self.product_id_2, 0.1).getData().getDiscountId()
        rId1 = self.proxy_market.addProductWeightRule(self.user_id1, self.store_id1, dId1, self.product_id, 1000, float('inf')).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityRule(self.user_id1, self.store_id1, dId1, "testCategory", 0, 5).getData().getRuleId()
        self.proxy_market.addCompositeRuleDiscountOr(self.user_id1, self.store_id1, dId1, rId1, rId2)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1100, userTransaction.getData().getTotalAmount())

    def test_addCondDiscountRule_OR_AND(self):
        dId1 = self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id1, self.product_id_2, 0.1).getData().getDiscountId()

        rId1 = self.proxy_market.addProductWeightRule(self.user_id1, self.store_id1, dId1, self.product_id, 1000, float('inf')).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityRule(self.user_id1, self.store_id1, dId1, "testCategory", 0, 5).getData().getRuleId()
        rId3 = self.proxy_market.addStoreTotalAmountRule(self.user_id1, self.store_id1, dId1, 2000, float('inf')).getData().getRuleId()

        rOr_id = self.proxy_market.addCompositeRuleDiscountOr(self.user_id1, self.store_id1, dId1, rId1, rId2).getData().getRuleId()
        self.proxy_market.addCompositeRuleDiscountAnd(self.user_id1, self.store_id1, dId1, rId3, rOr_id)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1100, userTransaction.getData().getTotalAmount())


if __name__ == '__main__':
    unittest.main()
