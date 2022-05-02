import unittest
import uuid
from Business.Bank import Bank
from Business.Address import Address
from Business.StorePackage.Product import Product
from Business.StorePackage.Store import Store


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.founderId = str(uuid.uuid4())
        bank = Bank(1, 1)
        address = Address("Israel", "Tel Aviv", "s", 1, 0)
        self.store = Store(0, "kfir store", self.founderId, bank, address)

        self.user1Id = str(uuid.uuid4())
        self.user2Id = str(uuid.uuid4())
        self.user3Id = str(uuid.uuid4())
        self.user4Id = str(uuid.uuid4())

        self.product1 = Product(0, "tara milk 5%", 10.0, "dairy", ["drink", "tara", "5%"])
        self.product2 = Product(1, "beef", 20.0, "meat", ["cow"])
        self.product3 = Product(2, "milk", 7.0, "dairy", ["drink"])
        self.product4 = Product(3, "yogurt", 15.5, "dairy", ["goat"])
        self.product5 = Product(4, "milk", 1.0, "dairy", [])

        # after the appointers we will get: manager = [user1->user2, founder->user1],
        #                                   owners = [founder, founder -> user1, user1->user3]

    def test_appoint_owners(self):
        self.store.appointOwnerToStore(self.founderId, self.user1Id)
        self.assertEqual(self.store.getStoreOwners(), [self.founderId, self.user1Id])

        self.store.appointOwnerToStore(self.user1Id, self.user3Id)
        self.assertEqual(self.store.getStoreOwners(), [self.founderId, self.user1Id, self.user3Id])

    def test_appoint_owners_FAIL(self):
        # user cannot assign himself
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.user1Id, self.user1Id))
        # user1 doesn't have the permission to assign user2
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.user1Id, self.user2Id))
        self.store.appointOwnerToStore(self.founderId, self.user1Id)
        # not allowed circularity
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.user1Id, self.founderId))
        self.store.appointOwnerToStore(self.user1Id, self.user2Id)
        # cannot assign user that all ready assigned
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.founderId, self.user2Id))

    def test_appoint_managers(self):
        self.test_appoint_owners()

        self.store.appointManagerToStore(self.user1Id, self.user2Id)
        self.assertEqual(self.store.getStoreManagers(), [self.user2Id])
        self.store.appointManagerToStore(self.founderId, self.user1Id)
        self.assertEqual(self.store.getStoreManagers(), [self.user2Id, self.user1Id])

    def test_appoint_managers_FAIL(self):
        # user cannot assign himself
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.user1Id, self.user1Id))
        # user1 doesn't have the permission to assign user2
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.user1Id, self.user2Id))
        self.store.appointManagerToStore(self.founderId, self.user1Id)
        # not allowed circularity
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.user1Id, self.founderId))
        self.store.appointOwnerToStore(self.founderId, self.user1Id)
        self.store.appointManagerToStore(self.user1Id, self.user2Id)
        # cannot assign user that all ready assigned
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.founderId, self.user2Id))

    def test_set_Permission(self):
        # because all the set-permission have the same code, we will only test once
        self.test_appoint_managers()
        self.store.setStockManagementPermission(self.user1Id, self.user2Id)
        self.assertTrue(self.store.getPermissions(self.user1Id).get(self.user2Id).hasPermission_StockManagement())

    def test_set_Permission_Fail(self):
        # not an owner
        self.assertRaises(Exception, lambda: self.store.setStockManagementPermission(self.user1Id, self.user2Id))
        self.test_appoint_managers()
        # doesnt have the permission to change permissions
        self.assertRaises(Exception, lambda: self.store.setStockManagementPermission(self.user2Id, self.user3Id))
        # first user didn't was the one how assign the second user
        self.assertRaises(Exception, lambda: self.store.setStockManagementPermission(self.user3Id, self.user2Id))

    def test_add_product(self):
        self.test_appoint_managers()
        self.store.addProductToStore(self.user1Id, self.product1)
        self.store.addProductToStore(self.user1Id, self.product2)
        self.store.addProductToStore(self.user3Id, self.product3)
        self.store.addProductToStore(self.user3Id, self.product4)
        self.store.addProductToStore(self.user3Id, self.product5)
        self.assertEqual({0: self.product1, 1: self.product2, 2: self.product3, 3: self.product4, 4: self.product5},
                         self.store.getProducts())

    def test_add_product_quantity(self):
        self.test_add_product()
        self.store.addProductQuantityToStore(self.user1Id, self.product1.getProductId(), 15)
        self.store.addProductQuantityToStore(self.user1Id, self.product2.getProductId(), 10)
        self.store.addProductQuantityToStore(self.user1Id, self.product3.getProductId(), 5)
        self.store.addProductQuantityToStore(self.user1Id, self.product4.getProductId(), 3)
        self.store.addProductQuantityToStore(self.user1Id, self.product5.getProductId(), 7)
        self.assertEqual({0: 15, 1: 10, 2: 5, 3: 3, 4: 7}, self.store.getProductQuantity())

    def test_remove_product(self):
        self.test_add_product_quantity()
        self.store.removeProductFromStore(self.user1Id, self.product1.getProductId())
        self.assertIsNone(self.store.getProducts().get(self.product1.getProductId()))

    def test_get_product_by_name(self):
        self.test_add_product_quantity()
        self.assertEqual([self.product3, self.product5], self.store.getProductsByName("milk"))
        self.assertEqual([self.product2], self.store.getProductsByName("beef"))
        self.assertEqual([], self.store.getProductsByName("lollipop"))

    def test_get_product_by_category(self):
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product3, self.product4, self.product5], self.store.getProductsByCategory("dairy"))
        self.assertEqual([self.product2], self.store.getProductsByCategory("meat"))
        self.assertEqual([], self.store.getProductsByCategory("candy"))

    def test_get_product_by_keyword(self):
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product3], self.store.getProductsByKeyword("drink"))
        self.assertEqual([self.product2], self.store.getProductsByKeyword("cow"))
        self.assertEqual([], self.store.getProductsByKeyword("dress"))

    def test_get_product_by_price_range(self):
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product2, self.product3, self.product4],
                         self.store.getProductsByPriceRange(7, 20.0))
        self.assertEqual([self.product2, self.product4], self.store.getProductsByPriceRange(15.0, 30.0))
        self.assertEqual([self.product3], self.store.getProductsByPriceRange(2.0, 9.0))
        self.assertEqual([self.product1], self.store.getProductsByPriceRange(10.0, 10.0))
        self.assertEqual([], self.store.getProductsByPriceRange(2.0, 5.0))
        self.assertEqual([], self.store.getProductsByPriceRange(9.0, 8.0))

    def test_add_quantity_product(self):
        self.test_add_product_quantity()
        self.assertTrue(self.store.addProductToBag(self.product4.getProductId(), 2))
        self.assertFalse(self.store.addProductToBag(self.product4.getProductId(), 2))

    def test_remove_quantity_product(self):
        self.test_add_product_quantity()
        self.store.removeProductFromBag(self.product4.getProductId(), 2)
        self.assertEqual(5, self.store.getProductQuantity().get(self.product4.getProductId()))
        self.store.removeProductFromBag(self.product4.getProductId(), 5)
        self.assertEqual(10, self.store.getProductQuantity().get(self.product4.getProductId()))


if __name__ == '__main__':
    unittest.main()
