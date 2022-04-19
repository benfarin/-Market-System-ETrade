import unittest
from Business.Bank import Bank
from Business.Address import Address
from Business.StorePackage.Product import Product
from Business.StorePackage.Store import Store
from Business.StorePackage.Cart import Cart
from Business.StorePackage.Bag import Bag


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.founderId = 0
        self.store = Store(0, "kfir store", 0, Bank(), Address())

        self.user1Id = 1
        self.user2Id = 2
        self.user3Id = 3
        self.user4Id = 4
        self.product1 = Product(0, "milk", 10.0, "dairy")
        self.product2 = Product(1, "milk", 7.0, "dairy")
        self.product2 = Product(2, "beef", 7.0, "meat")
        self.Cart_user1 = Cart(self.user1Id)
        self.Cart_user2 = Cart(self.user2Id)
        self.bag1 = Bag(self.Cart_user1, 0)
        self.bag2 = Bag(self.Cart_user2, 0)

        # after the appointers we will get: manager = [founder->user2, user2->user1],
        #                                   owners = [founder, founder -> user1, user1->user3]

    def test_appoint_owners(self):
        self.store.appointOwnerToStore(self.founderId, self.user1Id)
        self.assertEqual(self.store.getStoreOwners(), [self.founderId, self.user1Id])

        self.store.appointOwnerToStore(self.user1Id, self.user3Id)
        self.assertEqual(self.store.getStoreOwners(), [self.founderId, self.user1Id, self.user3Id])

    def test_appoint_owners_FAIL(self):
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.user1Id, self.user1Id))
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.user1Id, self.user2Id))
        self.store.appointOwnerToStore(self.founderId, self.user1Id)
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.user1Id, self.founderId))
        self.store.appointOwnerToStore(self.user1Id, self.user2Id)
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.founderId, self.user2Id))

    def test_appoint_managers(self):
        self.test_appoint_owners()

        self.store.appointManagerToStore(self.user1Id, self.user2Id)
        self.assertEqual(self.store.getStoreManagers(), [self.user2Id])
        self.store.appointManagerToStore(self.founderId, self.user1Id)
        self.assertEqual(self.store.getStoreManagers(), [self.user2Id, self.user1Id])

    def test_appoint_managers_FAIL(self):
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.user1Id, self.user1Id))
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.user1Id, self.user2Id))
        self.store.appointManagerToStore(self.founderId, self.user1Id)
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.user1Id, self.founderId))
        self.store.appointOwnerToStore(self.founderId, self.user1Id)
        self.store.appointManagerToStore(self.user1Id, self.user2Id)
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.founderId, self.user2Id))

    def test_print_rolesPermission(self):
        self.test_appoint_managers()
        print(self.store.getRolesInformation(self.user1Id))


if __name__ == '__main__':
    unittest.main()
