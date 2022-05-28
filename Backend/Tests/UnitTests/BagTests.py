import unittest
from unittest.mock import patch, MagicMock

from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.bag = Bag(0, 0)
        self.bag2 = Bag(1, 0)
        self.p1 = Product(0, 0, "Test", 50, "Category", 5, [])
        self.p2 = Product(1, 0, "Test1", 100, "Category", 5, [])
        self.discount = ProductDiscount(0, 0, 0.5)

    def test_calc_sum(self):
        self.bag.addProduct(self.p1.getModel(), 4)
        self.bag.addProduct(self.p2.getModel(), 2)
        self.assertEqual(400, self.bag.calcSum(None))
        self.assertEqual(300, self.bag.calcSum([self.discount]))
        # self.bag.addProduct(self.p1, 3)
        # self.assertEqual(70.0, self.bag.calcSum())
        # self.bag.addProduct(self.p2, 2)
        # self.assertEqual(110.0, self.bag.calcSum())

    def test_all(self):
        self.bag2.addProduct(self.p1.getModel(), 2)
        self.bag2.addProduct(self.p1.getModel(), 1)
        self.bag2.addProduct(self.p2.getModel(), 3)

        self.assertEqual(450, self.bag2.calcSum(None))
        self.assertEqual(3, self.bag2.removeProduct(self.p1.getProductId()))

        self.bag2.updateBag(self.p2.getProductId(), 2)
        self.assertEqual(500.0, self.bag2.calcSum(None))

        self.bag2.updateBag(self.p2.getProductId(), -2)
        self.assertEqual(300.0, self.bag2.calcSum(None))

        self.bag2.cleanBag()
        self.assertEqual(self.bag2.isEmpty(), True)

    def tearDown(self):
        self.bag.removeBag()
        self.bag2.removeBag()
        self.p1.removeProduct()
        self.p2.removeProduct()
        self.discount.removeDiscount()


if __name__ == '__main__':
    unittest.main()
