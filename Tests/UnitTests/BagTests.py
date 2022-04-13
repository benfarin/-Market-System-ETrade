import unittest
from Business.StorePackage.Bag import Bag
from Business.StorePackage.Cart import Cart
from Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.cart = Cart(0)
        self.cart.addBag(1)

        self.bag = self.cart.getBag(1)
        self.p1 = Product(1, "milk", 10, "1")
        self.p2 = Product(2, "meat", 20, "1")

    def test_isEmpty(self):
        self.assertTrue(self.bag.isEmpty())
        self.bag.addProduct(self.p1, 2)
        self.assertFalse(self.bag.isEmpty())
        self.bag.removeProduct(self.p1.getProductId())
        self.assertTrue(self.bag.isEmpty())

    def test_add_product(self):
        self.assertEqual(self.bag.getProducts(), {})
        self.bag.addProduct(self.p1, 2)
        self.assertEqual(self.bag.getProducts(), {self.p1: 2})
        self.bag.addProduct(self.p2, 3)
        self.assertEqual(self.bag.getProducts(), {self.p1: 2, self.p2: 3})
        self.bag.addProduct(self.p1, 4)
        self.assertEqual(self.bag.getProducts(), {self.p1: 6, self.p2: 3})

    def test_add_product_with_neg_quantity(self):
        self.assertRaises(Exception, lambda: self.bag.addProduct(self.p1, -1))

    def test_remove_product(self):
        self.bag.addProduct(self.p1, 2)
        self.bag.addProduct(self.p2, 3)

        self.bag.removeProduct(self.p2.getProductId())
        self.assertEqual(self.bag.getProducts(), {self.p1: 2})
        self.bag.removeProduct(self.p1.getProductId())
        self.assertEqual(self.bag.getProducts(), {})

    def test_remove_product_with_incorrect_productId(self):
        self.assertRaises(Exception, lambda: self.bag.removeProduct(3))

    def test_remove_product_quantity(self):
        self.bag.addProduct(self.p1, 4)
        self.bag.addProduct(self.p2, 2)

        self.bag.removeProductQuantity(self.p1.getProductId(), 1)
        self.assertEqual(self.bag.getProducts(), {self.p1: 3, self.p2: 2})

        self.bag.removeProductQuantity(self.p1.getProductId(), 3)
        self.assertEqual(self.bag.getProducts(), {self.p2: 2})

        self.bag.removeProductQuantity(self.p2.getProductId(), 4)
        self.assertEqual(self.bag.getProducts(), {})

    def test_remove_product_quantity_with_incorrect_productId(self):
        self.assertRaises(Exception, lambda: self.bag.removeProductQuantity(3, -1))
        self.assertRaises(Exception, lambda: self.bag.removeProductQuantity(3, 3))

    def test_calc_sum(self):
        self.bag.addProduct(self.p1, 4)
        self.assertEqual(40.0, self.bag.calcSum())
        self.bag.addProduct(self.p1, 3)
        self.assertEqual(70.0, self.bag.calcSum())
        self.bag.addProduct(self.p2, 2)
        self.assertEqual(110.0, self.bag.calcSum())

    def test_all(self):
        self.bag = Bag(self.cart, 1)
        self.bag.addProduct(self.p1, 2)
        self.bag.addProduct(self.p2, 3)
        self.assertEqual(self.bag.calcSum(), 80.0)
        self.bag.removeProduct(self.p1.getProductId())
        self.bag.removeProductQuantity(self.p2.getProductId(), 1)
        self.assertEqual(self.bag.calcSum(), 40.0)


if __name__ == '__main__':
    unittest.main()
