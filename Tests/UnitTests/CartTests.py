import unittest
from unittest.mock import patch, MagicMock
from Business.StorePackage.Cart import Cart


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.cart = Cart(0)

        self.p1 = MagicMock()
        self.p1.getProductId = MagicMock()
        self.p1.getProductId.return_value = 1
        self.p1.getProductPrice = MagicMock()
        self.p1.getProductPrice.return_value = 10.0

        self.p2 = MagicMock()
        self.p2.getProductId = MagicMock()
        self.p2.getProductId.return_value = 2
        self.p2.getProductPrice = MagicMock()
        self.p2.getProductPrice.return_value = 20.0

    def test_calcSum(self):
        self.cart.addProduct(1, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)
        self.cart.addProduct(2, self.p2, 5)

        self.assertEqual(150.0, self.cart.calcSum())

    def test_all(self):
        self.cart.addProduct(1, self.p1, 1)
        self.cart.addProduct(1, self.p2, 2)
        self.cart.addProduct(2, self.p2, 5)

        self.cart.removeBag(1)

        self.cart.updateProduct(2, self.p2.getProductId(), 2)
        self.assertEqual(140.0, self.cart.calcSum())
        self.cart.updateProduct(2, self.p2.getProductId(), -2)
        self.assertEqual(100.0, self.cart.calcSum())

        bag = MagicMock()
        bag.getStoreId.return_value = 2
        bag.calcSum.return_value = 120.0

        self.cart.updateBag(bag)
        self.assertEqual(120.0, self.cart.calcSum())


if __name__ == '__main__':
    unittest.main()
