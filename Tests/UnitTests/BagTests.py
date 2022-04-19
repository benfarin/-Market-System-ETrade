import unittest
from interfaces.ICart import ICart
from interfaces.IBag import IBag
from Business.StorePackage.Bag import Bag
from Business.StorePackage.Cart import Cart
from Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.cart: ICart = Cart(0)
        self.cart.addBag(1)

        self.bag: IBag = self.cart.getBag(1)
        self.p1 = Product(1, "milk", 10, "1")
        self.p2 = Product(2, "meat", 20, "1")

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
        self.assertEqual(2, self.bag.removeProduct(self.p1.getProductId()))

        self.bag.updateProduct(self.p2.getProductId(), 2)
        self.assertEqual(self.bag.calcSum(), 100.0)

        self.bag.updateProduct(self.p2.getProductId(), -2)
        self.assertEqual(self.bag.calcSum(), 60.0)


if __name__ == '__main__':
    unittest.main()
