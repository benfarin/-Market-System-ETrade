import unittest
from unittest.mock import patch, MagicMock

from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.bag = Bag(0)
        self.product = Product(0, 0, "Test", 50, "Category", 5, [])
        self.discount = ProductDiscount(0, 0, 0.5)

    def test_calc_sum(self):
        self.bag.addProduct(self.product.getModel(), 4)
        self.assertEqual(200, self.bag.calcSum(None))
        self.assertEqual(100, self.bag.calcSum([self.discount]))
        # self.bag.addProduct(self.p1, 3)
        # self.assertEqual(70.0, self.bag.calcSum())
        # self.bag.addProduct(self.p2, 2)
        # self.assertEqual(110.0, self.bag.calcSum())

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
