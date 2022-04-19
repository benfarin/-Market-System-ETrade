import unittest
from Business.Bank import Bank
from Business.Address import Address
from Business.StorePackage.Product import Product
from Business.StorePackage.Store import Store
from Business.StorePackage.Cart import Cart
from interfaces.IStore import IStore
from interfaces.ICart import ICart
from Business.Transactions.Transaction import Transaction


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.founderId = 0
        self.store: IStore = Store(0, "kfir store", 0, Bank(1, 1), Address("", "", "", 1, 1))

        self.user1Id = 1
        self.user2Id = 2
        self.user3Id = 3
        self.user4Id = 4

        self.cart_user1: ICart = Cart(self.user1Id)
        self.cart_user1.addBag(0)
        self.cart_user2: ICart = Cart(self.user2Id)
        self.cart_user2.addBag(0)
        self.product1 = Product(0, "milk", 10.0, "dairy")
        self.product2 = Product(1, "beef", 20.0, "meat")
        self.product3 = Product(2, "milk", 7.0, "dairy")
        self.product4 = Product(3, "yogurt", 15.5, "dairy")

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
        newProduct = Product(1, 'milk', 5.0, "dairy")
        self.store.updateProductFromStore(self.user1Id, self.product1.getProductId(), newProduct)
        self.assertEqual(newProduct, self.store.getProducts().get(self.product1.getProductId()))

    def test_print_rolesPermission(self):
        self.test_appoint_managers()
        print(self.store.PrintRolesInformation(self.user1Id))

    def test_print_PurchaseHistoryInformation(self):
        self.test_add_product_quantity()
        transaction1 = Transaction(1, 2, 0, {self.product1: 2, self.product2: 3}, 80.0)
        transaction2 = Transaction(2, 2, 0, {self.product1: 3, self.product3: 1}, 37.0)
        transaction3 = Transaction(2, 4, 0, {self.product1: 3, self.product3: 1}, 37.0)
        self.store.addTransaction(transaction1)
        self.store.addTransaction(transaction2)
        self.store.addTransaction(transaction3)
        print(self.store.printPurchaseHistoryInformation(self.user1Id))

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
