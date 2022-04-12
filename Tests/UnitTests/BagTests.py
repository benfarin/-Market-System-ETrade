import unittest
from Business.StorePackage.Bag import Bag
from Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):

    def test_calcSum(self):
        b = Bag()
        p1 = Product(1, "milk", 10, "1")
        p2 = Product(2, "meat", 20, "1")
        b.addProduct(p1, 2)
        b.addProduct(p2, 3)
        self.assertEqual(b.calcSum(), 80.0)
        b.removeProduct(p1.getProductId())
        b.removeProductQuantity(p2, 1)
        self.assertEqual(b.calcSum(), 40.0)


if __name__ == '__main__':
    unittest.main()
