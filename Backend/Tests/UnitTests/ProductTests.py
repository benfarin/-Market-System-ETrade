import unittest

from Backend.Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):

    def test_productGetters(self):
        product = Product(0, 2, "TestProduct", 50, "TestCategory", 5, ["Check", "Check2"])
        self.assertEqual(product.getProductId(), 0)
        self.assertEqual(product.getProductWeight(), 5)
        self.assertEqual(product.getProductPrice(), 50)
        self.assertEqual(product.getProductStoreId(), 2)
        self.assertEqual(product.getProductCategory(), "TestCategory")
        self.assertEqual(product.getProductName(), "TestProduct")
        self.assertEqual(product.getProductKeywords(), ["Check" , "Check2"])

    def test_productSetters(self):
        product = Product(0, 2, "TestProduct", 50, "TestCategory", 5, ["Check", "Check2"])
        product.setProductCategory("Category1")
        product.setProductWeight(100)
        product.setProductPrice(1)
        product.setProductName("TestProduct2")
        self.assertEqual(product.getProductWeight(), 100)
        self.assertEqual(product.getProductPrice(), 1)
        self.assertEqual(product.getProductCategory(), "Category1")
        self.assertEqual(product.getProductName(), "TestProduct2")


if __name__ == '__main__':
    unittest.main()
