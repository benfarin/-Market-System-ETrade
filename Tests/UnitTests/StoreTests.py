import unittest
from unittest.mock import patch, MagicMock
from Business.StorePackage.Store import Store
from Business.Transactions.Transaction import Transaction


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.founderId = 0
        self.store = Store(0, "kfir store", 0, MagicMock(), MagicMock())

        self.user1Id = 1
        self.user2Id = 2
        self.user3Id = 3
        self.user4Id = 4

        self.product1 = MagicMock()
        self.product1.getProductId = MagicMock()
        self.product1.getProductId.return_value = 0
        self.product1.getProductName = MagicMock()
        self.product1.getProductName.return_value = "milk"
        self.product1.getProductPrice = MagicMock()
        self.product1.getProductPrice.return_value = 10.0
        self.product1.category = MagicMock()
        self.product1.getProductCategory.return_value = "dairy"

        self.product2 = MagicMock()
        self.product2.getProductId = MagicMock()
        self.product2.getProductId.return_value = 1
        self.product2.getProductName = MagicMock()
        self.product2.getProductName.return_value = "beef"
        self.product2.getProductPrice = MagicMock()
        self.product2.getProductPrice.return_value = 20.0
        self.product2.category = MagicMock()
        self.product2.getProductCategory.return_value = "meat"

        self.product3 = MagicMock()
        self.product3.getProductId = MagicMock()
        self.product3.getProductId.return_value = 2
        self.product3.getProductName = MagicMock()
        self.product3.getProductName.return_value = "milk"
        self.product3.getProductPrice = MagicMock()
        self.product3.getProductPrice.return_value = 7.0
        self.product3.category = MagicMock()
        self.product3.getProductCategory.return_value = "dairy"

        self.product4 = MagicMock()
        self.product4.getProductId = MagicMock()
        self.product4.getProductId.return_value = 3
        self.product4.getProductName = MagicMock()
        self.product4.getProductName.return_value = "yogurt"
        self.product4.getProductPrice = MagicMock()
        self.product4.getProductPrice.return_value = 15.5
        self.product4.category = MagicMock()
        self.product4.getProductCategory.return_value = "dairy"

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
        self.assertEqual({0: self.product1, 1: self.product2, 2: self.product3, 3: self.product4},
                         self.store.getProducts())

    def test_add_product_quantity(self):
        self.test_add_product()
        self.store.addProductQuantityToStore(self.user1Id, self.product1.getProductId(), 15)
        self.store.addProductQuantityToStore(self.user1Id, self.product2.getProductId(), 10)
        self.store.addProductQuantityToStore(self.user1Id, self.product3.getProductId(), 5)
        self.store.addProductQuantityToStore(self.user1Id, self.product4.getProductId(), 3)
        self.assertEqual({0: 15, 1: 10, 2: 5, 3: 3}, self.store.getProductQuantity())

    def test_remove_product(self):
        self.test_add_product_quantity()
        self.store.removeProductFromStore(self.user1Id, self.product1.getProductId())
        self.assertIsNone(self.store.getProducts().get(self.product1.getProductId()))

    def test_update_product(self):
        self.test_add_product_quantity()

        newProduct = MagicMock()
        newProduct.getProductId = MagicMock()
        newProduct.getProductId.return_value = 2
        newProduct.getProductName = MagicMock()
        newProduct.getProductName.return_value = "milk"
        newProduct.getProductPrice = MagicMock()
        newProduct.getProductPrice.return_value = 7.0
        newProduct.category = MagicMock()
        newProduct.getProductCategory.return_value = "dairy"

        self.store.updateProductFromStore(self.user1Id, self.product1.getProductId(), newProduct)
        self.assertEqual(newProduct, self.store.getProducts().get(self.product1.getProductId()))

    def test_get_product_by_name(self):
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product3], self.store.getProductsByName("milk"))
        self.assertEqual([self.product2], self.store.getProductsByName("beef"))
        self.assertEqual([], self.store.getProductsByName("lollipop"))

    def test_get_product_by_category(self):
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product3, self.product4], self.store.getProductsByCategory("dairy"))
        self.assertEqual([self.product2], self.store.getProductsByCategory("meat"))
        self.assertEqual([], self.store.getProductsByCategory("candy"))

    def test_get_product_by_price_range(self):
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product2, self.product3, self.product4],
                         self.store.getProductsByPriceRange(7, 20.0))
        self.assertEqual([self.product2, self.product4], self.store.getProductsByPriceRange(15.0, 30.0))
        self.assertEqual([self.product3], self.store.getProductsByPriceRange(0.0, 9.0))
        self.assertEqual([self.product1], self.store.getProductsByPriceRange(10.0, 10.0))
        self.assertEqual([], self.store.getProductsByPriceRange(0.0, 5.0))
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
