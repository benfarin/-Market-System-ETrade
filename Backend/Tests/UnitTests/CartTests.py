import unittest
from unittest.mock import patch, MagicMock

from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount
from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Cart import Cart
from Backend.Business.StorePackage.Product import Product
from Backend.Exceptions.CustomExceptions import NoSuchStoreException


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.cart = Cart(0)
        self.cart2 = Cart(1)
        self.bag = Bag(0, 0)
        self.bag_2 = Bag(1, 0)
        self.p1 = Product(0, 0, "Test", 50, "Category", 5, [])
        self.p2 = Product(1, 1, "Test1", 100, "Category", 5, [])

    def testSimple(self):
        self.assertEqual(0, self.cart.getUserId())

        self.cart.addProduct(0, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)
        self.assertEqual(self.cart.getAllBags(), {0: self.bag, 1: self.bag_2})
        self.assertEqual(self.cart.getBag(1), self.bag_2)

        self.cart.cleanBag(1)
        self.assertEqual(self.cart.getBag(1).getProducts(), {})

        self.cart.removeBag(1)
        self.assertEqual(self.cart.getAllBags(), {0: self.bag})

    def test_updateCart(self):
        self.cart.addProduct(0, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)

        self.cart2.addProduct(0, self.p1, 1)
        self.cart2.updateCart(self.cart)

        self.assertEqual(self.cart2.getBag(0).getProducts(), {self.p1: 2})
        self.assertEqual(self.cart2.getBag(1).getProducts(), {self.p2: 2})

        self.assertEqual(self.cart2.getAllProductsByStore(), {0: {self.p1: 2}, 1: {self.p2: 2}})
        self.assertEqual(self.cart2.getAllProducts(), {self.p1: 2, self.p2: 2})

        self.cart.removeProduct(0, self.p1.getProductId())
        self.cart.removeProduct(1, self.p2.getProductId())
        self.cart2.removeProduct(0, self.p1.getProductId())

    def test_updateBag(self):
        self.cart.addProduct(0, self.p1, 7)
        self.assertFalse(self.cart2.updateBag(self.bag))

        bag3 = Bag(0, 2)
        bag3.addProduct(self.p1, 7)
        self.cart.updateBag(self.bag)
        self.assertEqual(self.cart.getBag(0).getProducts(), {self.p1: 7})

        self.cart.removeProduct(0, self.p1.getProductId())

    def test_calcSum(self):
        self.cart.addProduct(0, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)

        self.assertEqual(50.0, self.cart.calcSumOfBag(0, None))
        self.assertEqual(200.0, self.cart.calcSumOfBag(1, None))

    def test_compositeDiscount_calcSum(self):
        self.cart.addProduct(0, self.p1, 10)

        discount1 = StoreDiscount(0, 0.5)
        discount2 = StoreDiscount(1, 0.3)
        discount3 = DiscountComposite(2, discount1, discount2, 'Max')
        discount4 = ProductDiscount(3, self.p1.getProductId(), 0.6)
        discount5 = DiscountComposite(4, discount3, discount4, 'XOR', 1)

        self.assertEqual(250, self.bag.calcSum([discount5]))

        discount1.remove()
        discount2.remove()
        discount3.remove()
        discount4.remove()
        discount5.remove()

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
        self.cart.removeCart()
        self.cart2.removeCart()
        self.p1.removeProduct()
        self.p2.removeProduct()


if __name__ == '__main__':
    unittest.main()
