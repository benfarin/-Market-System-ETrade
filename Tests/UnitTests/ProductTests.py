import unittest

from Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):
    def test_something(self):
        product = Product(0, "TestProduct", 100, "TestCategory")
        self.assertEqual(product.getProductId(), 0)


if __name__ == '__main__':
    unittest.main()
