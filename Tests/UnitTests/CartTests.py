import unittest
from interfaces.ICart import ICart
from interfaces.IBag import IBag
from Business.StorePackage.Bag import Bag
from Business.StorePackage.Cart import Cart
from Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.cart: ICart = Cart(0)
        self.p1 = Product(1, "milk", 10, "1")
        self.p2 = Product(2, "meat", 20, "1")

    def test_calcSum(self):
        self.cart.addBag(1)
        self.cart.addBag(2)
        self.bag1 = self.cart.getBag(1)
        self.cart.addProduct(1, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)
        self.bag2 = self.cart.getBag(1)
        self.cart.addProduct(2, self.p2, 5)

        self.assertEqual(150.0, self.cart.calcSum())

    def test_all(self):
        self.cart.addBag(1)
        self.cart.addBag(2)
        self.bag1 = self.cart.getBag(1)
        self.cart.addProduct(1, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)
        self.bag2 = self.cart.getBag(1)
        self.cart.addProduct(2, self.p2, 5)

        self.cart.removeBag(1)

        self.cart.updateProduct(2, self.p2.getProductId(), 2)
        self.assertEqual(140.0, self.cart.calcSum())
        self.cart.updateProduct(2, self.p2.getProductId(), -2)
        self.assertEqual(100.0, self.cart.calcSum())

        bag: IBag = Bag(0, 2)
        bag.addProduct(self.p1, 10)
        self.cart.updateBag(bag)

        self.assertEqual(100.0, self.cart.calcSum())


if __name__ == '__main__':
    unittest.main()
