import unittest

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.discountCategory = CategoryDiscount(0, "Electric", 0.5)
        self.discountProduct = ProductDiscount(1, 0, 0.85)
        self.discountStore = StoreDiscount(3, 0.1)
        self.discountComposite = DiscountComposite(5, self.discountCategory.getModel(), self.discountProduct.getModel(), 'Max', 1)


    def test_DiscountGetters(self):
        self.assertEqual(self.discountCategory.getDiscountId(), 0)
        self.assertEqual(self.discountCategory.getDiscountPercent(), 0.5)
        self.assertEqual(self.discountCategory.getCategory(), "Electric")

        self.assertEqual(self.discountProduct.getDiscountId(), 1)
        self.assertEqual(self.discountProduct.getDiscountPercent(), 0.85)
        self.assertEqual(self.discountProduct.getProductId(), 0)

        self.assertEqual(self.discountStore.getDiscountId(), 3)
        self.assertEqual(self.discountStore.getDiscountPercent(), 0.1)

        self.assertEqual(self.discountComposite.getDiscountId(), 5)
        self.assertEqual(self.discountComposite.getDiscount1(), 0)
        self.assertEqual(self.discountComposite.getDiscount2(), 1)
        self.assertEqual(self.discountComposite.getDiscountType(), 'Max')

    def tearDown(self):
        self.discountCategory.remove()
        self.discountComposite.remove()
        self.discountProduct.remove()
        self.discountStore.remove()






if __name__ == '__main__':
    unittest.main()
