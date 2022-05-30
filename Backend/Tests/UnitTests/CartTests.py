import unittest
from unittest.mock import patch, MagicMock

from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Cart import Cart
from Backend.Business.StorePackage.Product import Product
from Backend.Exceptions.CustomExceptions import NoSuchStoreException


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.cart = Cart(0)
        self.bag = Bag(0, 0)
        self.bag_2 = Bag(1, 0)
        self.p1 = Product(0, 0, "Test", 50, "Category", 5, [])
        self.p2 = Product(1, 1, "Test1", 100, "Category", 5, [])

    def testSimple(self):
        self.assertEqual(0, self.cart.getUserId())

        self.cart.addProduct(0, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)
        self.assertEqual(self.cart.getAllBags(), [self.bag, self.bag_2])
        self.assertEqual(self.cart.getBag(1), self.bag_2)

        self.cart.cleanBag(1)
        self.assertEqual(self.cart.getBag(1).getProducts(), {})

        self.cart.removeBag(1)
        self.assertEqual(self.cart.getAllBags(), [self.bag])

    def test_updateCart(self):
        c = Cart(0)
        c.addProduct(0, self.p1, 1)
        c.updateCart(self.cart)
        self.assertEqual(c.getBag(0).getProducts(), {self.p1: 2})
        self.assertEqual(c.getBag(1).getProducts(), {self.p2: 1})

        c.removeCart()

    def test_calcSum(self):
        self.cart.addProduct(0, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)

        self.assertEqual(50.0, self.cart.calcSumOfBag(0, None))
        self.assertEqual(200.0, self.cart.calcSumOfBag(1, None))

    def test_all(self):
        self.cart.addProduct(0, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)
        self.cart.addProduct(1, self.p2, 5)

        self.assertEqual(50.0, self.cart.calcSumOfBag(0, None))
        self.cart.removeBag(0)

        self.cart.updateProduct(1, self.p2.getProductId(), 2)
        self.assertEqual(900.0, self.cart.calcSumOfBag(1, None))
        self.cart.updateProduct(1, self.p2.getProductId(), -2)
        self.assertEqual(700.0, self.cart.calcSumOfBag(1, None))

        self.assertEqual(self.cart.removeProduct(1, self.p2.getProductId()), 7)

        self.cart.cleanCart()
        self.assertEqual(self.cart.isEmpty(), True)

    def tearDown(self):
        self.p1.removeProduct()
        self.p2.removeProduct()
        self.bag.removeBag()
        self.bag_2.removeBag()
        self.cart.removeCart()


if __name__ == '__main__':
    unittest.main()
