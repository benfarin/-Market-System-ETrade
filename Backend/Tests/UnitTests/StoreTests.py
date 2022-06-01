import threading
import unittest
from collections import Counter

from Backend.Business.Bank import Bank
from Backend.Business.Address import Address
from Backend.Business.UserPackage.Member import Member
from Backend.Business.StorePackage.Product import Product
from Backend.Business.StorePackage.Store import Store


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.bank = Bank(1, 1)
        self.address = Address("Israel", "Tel Aviv", "s", 1, 0)

        self.founder = Member("kfir0", "1234", "012", self.address, self.bank)
        self.store = Store(0, "kfir store", self.founder, self.bank, self.address)

        self.member1 = Member("kfir1", "1234", "012", self.address, self.bank)
        self.member2 = Member("kfir2", "1234", "012", self.address, self.bank)
        self.member3 = Member("kfir3", "1234", "012", self.address, self.bank)
        self.member4 = Member("kfir4", "1234", "012", self.address, self.bank)

        self.product1 = Product(0, 0, "tara milk 5%", 10.0, "dairy", 0.5, ["drink", "tara", "5%"])
        self.product2 = Product(1, 0, "beef", 20.0, "meat", 2, ["cow"])
        self.product3 = Product(2, 0, "milk", 7.0, "dairy", 0.3, ["drink"])
        self.product4 = Product(3, 0, "yogurt", 15.5, "dairy", 0.1, ["goat"])
        self.product5 = Product(4, 0, "milk", 1.0, "dairy", 0.3, [])

        # after the appointers we will get: manager = [user1->user2, founder->user1],
        #                                   owners = [founder, founder -> user1, user1->user3]

    def test_appoint_owners(self):  ###WORKING
        self.store.appointOwnerToStore(self.founder, self.member1)
        self.assertEqual(Counter(self.store.getStoreOwners()) == Counter([self.founder, self.member1]), True)

        self.store.appointOwnerToStore(self.member1, self.member3)
        self.assertEqual(Counter(self.store.getStoreOwners()) == Counter([self.founder, self.member1, self.member3]),
                         True)

    def test_appoint_owners_FAIL(self):  ###WORKING
        # user cannot assign himself
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.founder, self.founder))
        # user1 doesn't have the permission to assign user2
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.member1, self.member2))
        self.store.appointOwnerToStore(self.founder, self.member1)
        # not allowed circularity
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.member1, self.founder))
        self.store.appointOwnerToStore(self.member1, self.member2)
        # cannot assign user that all ready assigned
        self.assertRaises(Exception, lambda: self.store.appointOwnerToStore(self.founder, self.member2))

    def test_remove_owner(self):  ###WORKING
        self.test_appoint_owners()
        try:
            print(self.store.getStoreOwners())
            self.store.removeStoreOwner(self.member1, self.member3)
            print(self.store.getStoreOwners())
            self.store.removeStoreOwner(self.founder, self.member1)
            print(self.store.getStoreOwners())
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_appoint_managers(self):  ###WORKING
        self.test_appoint_owners()

        self.store.appointManagerToStore(self.member1, self.member2)
        self.assertEqual(Counter(self.store.getStoreManagers()) == Counter([self.member2]), True)
        self.store.appointManagerToStore(self.founder, self.member1)
        self.assertEqual(Counter(self.store.getStoreManagers()) == Counter([self.member2, self.member1]), True)

    def test_appoint_managers_FAIL(self):  ###WORKING
        # user cannot assign himself
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.member1, self.member1))
        # user1 doesn't have the permission to assign user2
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.member1, self.member2))
        self.store.appointManagerToStore(self.founder, self.member1)
        # not allowed circularity
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.member1, self.founder))
        self.store.appointOwnerToStore(self.founder, self.member1)
        self.store.appointManagerToStore(self.member1, self.member2)
        # cannot assign user that all ready assigned
        self.assertRaises(Exception, lambda: self.store.appointManagerToStore(self.founder, self.member2))

    def test_set_Permission(self):  ###WORKING
        # because all the set-permission have the same code, we will only test once
        self.test_appoint_managers()
        self.store.setStockManagementPermission(self.member1, self.member3)
        self.assertTrue(self.store.getPermissions(self.member1).stockManagement)

    def test_set_Permission_Fail(self):  ###WORKING
        # not an owner
        self.assertRaises(Exception, lambda: self.store.setStockManagementPermission(self.member1, self.member1))
        self.test_appoint_managers()
        # doesnt have the permission to change permissions
        self.assertRaises(Exception, lambda: self.store.setStockManagementPermission(self.member3, self.member2))
        # first user didn't was the one how assign the second user
        self.assertRaises(Exception, lambda: self.store.setStockManagementPermission(self.member3, self.member1))

    def test_add_product(self):  ###WORKING
        self.test_appoint_managers()
        self.store.addProductToStore(self.member1, self.product1)
        self.store.addProductToStore(self.member1, self.product2)
        self.store.addProductToStore(self.member3, self.product3)
        self.store.addProductToStore(self.member3, self.product4)
        self.store.addProductToStore(self.member3, self.product5)
        self.assertEqual({0: self.product1, 1: self.product2, 2: self.product3, 3: self.product4, 4: self.product5},
                         self.store.getProducts())

    def test_add_product_quantity(self):  ###WORKING
        self.test_add_product()
        self.store.addProductQuantityToStore(self.member1, self.product1.getProductId(), 15)
        self.store.addProductQuantityToStore(self.member1, self.product2.getProductId(), 10)
        self.store.addProductQuantityToStore(self.member1, self.product3.getProductId(), 5)
        self.store.addProductQuantityToStore(self.member1, self.product4.getProductId(), 3)
        self.store.addProductQuantityToStore(self.member1, self.product5.getProductId(), 7)
        self.assertEqual({0: 15, 1: 10, 2: 5, 3: 3, 4: 7}, self.store.getProductQuantity())

    def test_remove_product(self):  ###WORKING
        self.test_add_product_quantity()
        self.store.removeProductFromStore(self.member1, self.product1.getProductId())
        self.assertIsNone(self.store.getProducts().get(self.product1.getProductId()))

    def test_get_product_by_name(self):   ###WORKING
        self.test_add_product_quantity()
        self.assertEqual([self.product3, self.product5], self.store.getProductsByName("milk"))
        self.assertEqual([self.product2], self.store.getProductsByName("beef"))
        self.assertEqual([], self.store.getProductsByName("lollipop"))

    def test_get_product_by_category(self): ###WORKING
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product3, self.product4, self.product5],
                         self.store.getProductsByCategory("dairy"))
        self.assertEqual([self.product2], self.store.getProductsByCategory("meat"))
        self.assertEqual([], self.store.getProductsByCategory("candy"))

    def test_get_product_by_keyword(self):  ###WORKING
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product3], self.store.getProductsByKeyword("drink"))
        self.assertEqual([self.product2], self.store.getProductsByKeyword("cow"))
        self.assertEqual([], self.store.getProductsByKeyword("dress"))

    def test_get_product_by_price_range(self):  ###WORKING
        self.test_add_product_quantity()
        self.assertEqual([self.product1, self.product2, self.product3, self.product4],
                         self.store.getProductsByPriceRange(7, 20.0))
        self.assertEqual([self.product2, self.product4], self.store.getProductsByPriceRange(15.0, 30.0))
        self.assertEqual([self.product3], self.store.getProductsByPriceRange(2.0, 9.0))
        self.assertEqual([self.product1], self.store.getProductsByPriceRange(10.0, 10.0))
        self.assertEqual([], self.store.getProductsByPriceRange(2.0, 5.0))
        self.assertEqual([], self.store.getProductsByPriceRange(9.0, 8.0))

    def test_add_quantity_product(self):  ###WORKING
        self.test_add_product_quantity()

        t1 = threading.Thread(target=self.store.addProductQuantityToStore,
                              args=(self.member1, self.product1.getProductId(), 10))
        t2 = threading.Thread(target=self.store.addProductQuantityToStore,
                              args=(self.member3, self.product1.getProductId(), 10))

        try:
            t1.start()
            t2.start()

            t1.join()
            t2.join()
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_remove_quantity_product(self):  ###WORKING
        self.test_add_product_quantity()
        self.store.removeProductFromBag(self.product4.getProductId(), 2)
        self.assertEqual(5, self.store.getProductQuantity().get(self.product4.getProductId()))
        self.store.removeProductFromBag(self.product4.getProductId(), 5)
        self.assertEqual(10, self.store.getProductQuantity().get(self.product4.getProductId()))

    def tearDown(self):
        self.bank.removeBank()
        self.address.removeAddress()

        self.founder.removeMember()
        self.store.removeStore()

        self.member1.removeMember()
        self.member2.removeMember()
        self.member3.removeMember()
        self.member4.removeMember()

        self.product1.removeProduct()
        self.product2.removeProduct()
        self.product3.removeProduct()
        self.product4.removeProduct()
        self.product5.removeProduct()


if __name__ == '__main__':
    unittest.main()
