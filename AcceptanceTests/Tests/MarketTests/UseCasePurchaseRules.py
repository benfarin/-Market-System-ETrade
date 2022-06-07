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
        admin_id = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(admin_id, "Manager", "1234")
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        __guestId2 = self.proxy_user.login_guest().getData().getUserID()
        __guestId3 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("Rotem", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                "Rager", 1, 0)
        self.proxy_user.register("Ori", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.proxy_user.register("Kfir", "1234", "0540000000", 123, 1, "Israel", "Beer Sheva",
                                 "Rager", 1, 0)
        self.user_id1 = self.proxy_user.login_member(self.__guestId1, "Rotem", "1234").getData().getUserID()
        self.user_id2 = self.proxy_user.login_member(self.__guestId1, "Ori", "1234").getData().getUserID()
        self.user_id3 = self.proxy_user.login_member(self.__guestId1, "Kfir", "1234").getData().getUserID()

        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.store_id1 = self.proxy_user.open_store("Rotem", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        self.store_id2 = self.proxy_user.open_store("Ori", self.user_id1, 123, 1, "Israel", "Beer Sheva",
                                                  "Rager", 1, 00000).getData().getStoreId()

        self.product_id = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct1", 10,
                                                               "testCategory", 20, ["test"]).getData().getProductId()
        self.product_id_2 = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct2", 100,
                                                                 "testCategory1", 17, ["test"]).getData().getProductId()
        self.product_id_3 = self.proxy_market.add_product_to_store(self.store_id1, self.user_id1, "testProduct3", 20,
                                                                 "testCategory", 15, ["test"]).getData().getProductId()
        self.product_id_4 = self.proxy_market.add_product_to_store(self.store_id2, self.user_id1, "testProduct4", 10,
                                                                 "testCategory", 15, ["test"]).getData().getProductId()

        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id, 100)
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id_2, 100)
        self.proxy_market.add_quantity_to_store(self.store_id1, self.user_id1, self.product_id_3, 100)
        self.proxy_market.add_quantity_to_store(self.store_id2, self.user_id1, self.product_id_4, 100)

    def tearDown(self) -> None:
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id1)
        self.proxy_market.removeStoreForGood(self.user_id1, self.store_id2)
        self.proxy_user.removeMember("Manager", "Rotem")
        self.proxy_user.removeMember("Manager", "Ori")
        self.proxy_user.removeMember("Manager", "Kfir")
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_addSimpleRuleStore(self):
        self.proxy_market.addStoreTotalAmountPurchaseRule(self.user_id1, self.store_id1, 100, 2000).getData()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")

        self.assertEqual(1100, userTransaction.getData().getTotalAmount())

    def test_addSimpleRuleStore_NotPassing(self):
        self.proxy_market.addStoreTotalAmountPurchaseRule(self.user_id1, self.store_id1, 1500, 10000).getData()

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")

        self.assertEqual(0, userTransaction.getData().getTotalAmount())

    def test_addCondPurchaseRule_AND(self):
        rId1 = self.proxy_market.addProductWeightPurchaseRule(self.user_id1, self.store_id1, self.product_id, 100, 100000).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityPurchaseRule(self.user_id1, self.store_id1, "testCategory", 0, 5).getData().getRuleId()
        self.proxy_market.addCompositeRulePurchaseAnd(self.user_id1, self.store_id1, rId1, rId2)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")

        self.assertEqual(0, userTransaction.getData().getTotalAmount())

    def test_addCondDiscountRule_OR(self):
        rId1 = self.proxy_market.addProductQuantityPurchaseRule(self.user_id1, self.store_id1, self.product_id, 5, 100000).getData().getRuleId()
        rId2 = self.proxy_market.addStoreQuantityPurchaseRule(self.user_id1, self.store_id1, 0, 30).getData().getRuleId()
        self.proxy_market.addCompositeRulePurchaseAnd(self.user_id1, self.store_id1, rId1, rId2)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")

        self.assertEqual(1100, userTransaction.getData().getTotalAmount())

    def test_addCondDiscountRule_OR_AND_with_discount(self):
        self.proxy_market.addSimpleDiscount_Product(self.user_id1, self.store_id1, self.product_id_2, 0.1).getData().getDiscountId()

        rId1 = self.proxy_market.addProductWeightPurchaseRule(self.user_id1, self.store_id1, self.product_id, 100, 100000).getData().getRuleId()
        rId2 = self.proxy_market.addCategoryQuantityPurchaseRule(self.user_id1, self.store_id1, "testCategory", 0, 5).getData().getRuleId()
        rId3 = self.proxy_market.addStoreTotalAmountPurchaseRule(self.user_id1, self.store_id1, 100, 100000).getData().getRuleId()

        rOr_id = self.proxy_market.addCompositeRulePurchaseOr(self.user_id1, self.store_id1, rId1, rId2).getData().getRuleId()
        self.proxy_market.addCompositeRulePurchaseAnd(self.user_id1, self.store_id1, rId3, rOr_id)

        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id, 10)
        self.proxy_user.add_product_to_cart(self.user_id1, self.store_id1, self.product_id_2, 10)
        userTransaction = self.proxy_user.purchase_product(self.user_id1, "1234123412341234", "2", "27", "Rotem", "123", "123")
        print(userTransaction)
        self.assertEqual(1000, userTransaction.getData().getTotalAmount())


if __name__ == '__main__':
    unittest.main()
