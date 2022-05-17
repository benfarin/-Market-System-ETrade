import sys
import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService
from Business.Rules.ruleCreator import ruleCreator


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

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        cls.store_id1 = cls.proxy_user.open_store("testStore1", cls.user_id1, 123, None, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        cls.product_id = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct1", 10,
                                                               "testCategory", 10, ["test"]).getData().getProductId()
        cls.product_id_2 = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct2", 100,
                                                                 "testCategory1", 10, ["test"]).getData().getProductId()
        cls.product_id_3 = cls.proxy_market.add_product_to_store(cls.store_id1, cls.user_id1, "testProduct3", 20,
                                                                 "testCategory", 10, ["test"]).getData().getProductId()
        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id, 100)
        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id_2, 100)
        cls.proxy_market.add_quantity_to_store(cls.store_id1, cls.user_id1, cls.product_id_3, 100)

    def test_addSimpleDiscountStoreAdd(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData()
        dId2 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData()
        self.proxy_market.addConditionDiscountAdd(self.user_id1, self.store_id1, dId1, dId2)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        # print(userTransaction.__str__())
        self.assertEqual(880, userTransaction.getData().getTotalAmount())

    def test_addSimpleDiscountStoreMax(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData()
        dId2 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, 0.5,
                                                            "testCategory1").getData()
        self.proxy_market.addConditionDiscountMax(self.user_id1, self.store_id1, dId1, dId2)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(600, userTransaction.getData().getTotalAmount())

    def test_addSimpleDiscountStoreXor(self):
        dId1 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, 0.1, "testCategory1").getData()

        self.rule_creator: ruleCreator = ruleCreator.getInstance()
        rule1 = self.proxy_market.createProductWeightRule(self.user_id1, self.store_id1, self.product_id, 110, 101).getData().getRuleId()
        rule2 = self.proxy_market.createStoreWeightRule(self.user_id1, self.store_id1, 1000, 90).getData().getRuleId()
        self.proxy_market.addConditionDiscountXor(self.user_id1, self.store_id1, dId1, rule1, rule2, 0)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1000, userTransaction.getData().getTotalAmount())

    def test_addSimpleDiscountStoreAnd(self):
        dId1 = self.proxy_market.addSimpleDiscount_Category(self.user_id1, self.store_id1, 0.1, "testCategory1").getData()

        rule1 = self.proxy_market.createStoreTotalAmountRule(self.user_id1, self.store_id1, 2000, 1000).getData().getRuleId()
        rule2 = self.proxy_market.createCategoryRule(self.user_id1, self.store_id1, "testCategory1", 100, 9).getData().getRuleId()
        self.proxy_market.addConditionDiscountAnd(self.user_id1, self.store_id1, dId1, rule1, rule2)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(1000, userTransaction.getData().getTotalAmount())

    def test_addSimpleDiscountStoreOr(self):
        dId1 = self.proxy_market.addSimpleDiscount_Store(self.user_id1, self.store_id1, 0.1).getData()

        rule1 = self.proxy_market.createStoreQuantityRule(self.user_id1, self.store_id1, 1000, 1).getData().getRuleId()
        rule2 = self.proxy_market.createProductRule(self.user_id1, self.store_id1, self.product_id_2, 100, 11).getData().getRuleId()

        self.proxy_market.addConditionDiscountOr(self.user_id1, self.store_id1, dId1, rule1, rule2)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)

        self.assertEqual(990, userTransaction.getData().getTotalAmount())

    def test_remove_Discount(self):
        dId1 = self.proxy_market.addSimpleConditionDiscount_Store(self.user_id1, self.store_id1, "quantity", 0.1, 100, 10).getData()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)
        self.assertEqual(990, userTransaction.getData().getTotalAmount())

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)

        self.proxy_market.removeDiscount(self.user_id1, self.store_id1, dId1)

        userTransaction = self.proxy_user.purchase_product(self.user_id1, 10, 10)
        self.assertEqual(1100, userTransaction.getData().getTotalAmount())


if __name__ == '__main__':
    unittest.main()
