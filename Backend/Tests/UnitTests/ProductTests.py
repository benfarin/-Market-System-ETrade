import unittest

from Backend.Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.product = Product(0, 2, "TestProduct", 50, "TestCategory", 5, ["Check", "Check2"])
        self.product2 = Product(1, 2, "TestProduct", 50, "TestCategory", 5, ["Check", "Check2"])

    def testCheckEQ(self):
        self.product_to_check = Product(model=self.product.getModel())
        self.assertEqual(self.product, self.product_to_check)
        self.product_to_check.removeProduct()


    def test_productGetters(self):
        self.assertEqual(self.product.getProductId(), 0)
        self.assertEqual(self.product.getProductWeight(), 5)
        self.assertEqual(self.product.getProductPrice(), 50)
        self.assertEqual(self.product.getProductStoreId(), 2)
        self.assertEqual(self.product.getProductCategory(), "TestCategory")
        self.assertEqual(self.product.getProductName(), "TestProduct")
        self.assertEqual(self.product.getProductKeywords(), ["Check" , "Check2"])

    def test_productSetters(self):
        self.product2.setProductCategory("Category1")
        self.product2.setProductWeight(100)
        self.product2.setProductPrice(1)
        self.product2.setProductName("TestProduct2")
        self.product2.addKeyWord("keyword")
        self.assertEqual(self.product2.getProductWeight(), 100)
        self.assertEqual(self.product2.getProductPrice(), 1)
        self.assertEqual(self.product2.getProductCategory(), "Category1")
        self.assertEqual(self.product2.getProductName(), "TestProduct2")
        self.assertEqual(self.product2.getProductKeywords(), ["Check", "Check2", "keyword"])
        self.assertEqual(self.product2.isExistsKeyword("Check2"), True)
        self.product2.removeKeyWord("Check2")
        self.assertEqual(self.product2.isExistsKeyword("Check2"), False)

    def tearDown(self):
        self.product.removeProduct()
        self.product2.removeProduct()


if __name__ == '__main__':
    unittest.main()
