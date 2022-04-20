import unittest
from unittest.mock import MagicMock
from Business.StorePackage.Bag import Bag


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.bag = Bag(0)

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

    def test_calc_sum(self):
        self.bag.addProduct(self.p1, 4)
        self.assertEqual(40.0, self.bag.calcSum())
        self.bag.addProduct(self.p1, 3)
        self.assertEqual(70.0, self.bag.calcSum())
        self.bag.addProduct(self.p2, 2)
        self.assertEqual(110.0, self.bag.calcSum())

    def test_all(self):
        self.bag.addProduct(self.p1, 2)
        self.bag.addProduct(self.p2, 3)

        self.assertEqual(80.0, self.bag.calcSum())
        self.assertEqual(2, self.bag.removeProduct(self.p1.getProductId()))

        self.bag.updateProduct(self.p2.getProductId(), 2)
        self.assertEqual(100.0, self.bag.calcSum())

        self.bag.updateProduct(self.p2.getProductId(), -2)
        self.assertEqual(60.0, self.bag.calcSum())


if __name__ == '__main__':
    unittest.main()
