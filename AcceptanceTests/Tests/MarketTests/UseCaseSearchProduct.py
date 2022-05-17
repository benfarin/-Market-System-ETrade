import unittest

from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService


class UseCaseSearchProduct(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.market_proxy = MarketProxyBridge(MarketRealBridge())
        self.user_proxy = UserProxyBridge(UserRealBridge())
        self.user_proxy.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                          "Ben Gurion", 1, 1)
        self.__guestId1 = self.user_proxy.login_guest().getData().getUserID()
        self.user_proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim")
        self.user_id = self.user_proxy.login_member(self.__guestId1, "user1", "1234").getData().getUserID()
        self.store_id = self.user_proxy.open_store("store", self.user_id, 0, 0, "israel", "Beer-Sheva", "Ben-Gurion",
                                   0, 1).getData().getStoreId()
        self.product1 = self.market_proxy.add_product_to_store(self.store_id, self.user_id, "Product", 500,
                                                      "Milk", 10, ["Test1", "Test2"]).getData()
        self.product2 = self.market_proxy.add_product_to_store(self.store_id, self.user_id, "Product2", 10,
                                                      "Meat", 10, ["Test3", "Test4"]).getData()

    def test_search_by_name(self):
        # need to modify for response in all functions
        self.assertEqual(self.market_proxy.search_product_name("Product").getData()[0].getProductId(), self.product1.getProductId())
        self.assertEqual(self.market_proxy.search_product_name("Product2").getData()[0].getProductId(), self.product2.getProductId())
        self.assertEqual(self.market_proxy.search_product_name("Product5").getData(), [])
        self.assertEqual(self.market_proxy.search_product_name("").getData(), [])

    def test_search_by_category(self):
        self.assertEqual(self.market_proxy.search_product_category("MILK").getData()[0].getProductId(), self.product1.getProductId())
        self.assertEqual(self.market_proxy.search_product_category("Meat").getData()[0].getProductId(), self.product2.getProductId())
        self.assertEqual(self.market_proxy.search_product_category("appLes").getData(), [])

    def test_search_by_price_range(self):
        products1 = self.market_proxy.search_product_price_range(5, 1000).getData()
        products_id1 = []
        for p in products1:
            products_id1.append(p.getProductId())
        self.assertEqual(products_id1, [self.product1.getProductId(), self.product2.getProductId()])  #two products in this range

        products2 = self.market_proxy.search_product_price_range(5488, 10000).getData()
        products_id2 = []
        for p in products2:
            products_id2.append(p.getProductId())
        self.assertEqual(products_id2, []) # no products in this range prices

    def test_search_by_keywords(self):
        self.assertEqual(self.market_proxy.search_product_keyWord("TeSt1").getData()[0].getProductId(), self.product1.getProductId())
        self.assertEqual(self.market_proxy.search_product_keyWord("TesT4").getData()[0].getProductId(), self.product2.getProductId())
        self.assertEqual(self.market_proxy.search_product_keyWord("Te").getData(), [])
        self.assertEqual(self.market_proxy.search_product_keyWord("").getData(), [])

    def test_search_by_name_negative(self):
        self.assertEqual(self.market_proxy.search_product_name("Product3").getData(), [])
        self.assertEqual(self.market_proxy.search_product_name("").getData(), [])
        self.assertEqual(self.market_proxy.search_product_name("235223sdf").getData(), [])

    def test_search_by_category_negative(self):
        self.assertEqual(self.market_proxy.search_product_category("Category999").getData(), [])
        self.assertEqual(self.market_proxy.search_product_category("").getData(), [])
        self.assertEqual(self.market_proxy.search_product_category("532532").getData(), [])

    def test_search_by_price_range_negative(self):
        self.assertEqual(self.market_proxy.search_product_price_range(2000, 3000).getData(), [])
        self.assertEqual(self.market_proxy.search_product_price_range(-1241, -200).getData(), [])

    def test_search_by_keywords_negative(self):
        self.assertEqual(self.market_proxy.search_product_keyWord("Test5").getData(), [])
        self.assertEqual(self.market_proxy.search_product_keyWord("").getData(), [])
        self.assertEqual(self.market_proxy.search_product_keyWord("21421").getData(), [])
        self.assertEqual(self.market_proxy.search_product_keyWord("Tes").getData(), [])


if __name__ == '__main__':
    unittest.main()
