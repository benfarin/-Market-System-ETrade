import unittest

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount


class MyTestCase(unittest.TestCase):
    def test_DiscountGetters(self):
        discountCategory = CategoryDiscount(0, "Electric", 0.5)
        discountProduct = ProductDiscount(1, 0, 0.85)
        discountStore = StoreDiscount(3, 0.1)
        discountComposite = DiscountComposite(5, discountCategory.getModel(), discountProduct.getModel(), 'Max', 1)

        self.assertEqual(discountCategory.getDiscountId(), 0)
        self.assertEqual(discountCategory.getDiscountPercent(), 0.5)
        self.assertEqual(discountCategory.getCategory(), "Electric")

        self.assertEqual(discountProduct.getDiscountId(), 1)
        self.assertEqual(discountProduct.getDiscountPercent(), 0.85)
        self.assertEqual(discountProduct.getProductId(), 0)

        self.assertEqual(discountStore.getDiscountId(), 3)
        self.assertEqual(discountStore.getDiscountPercent(), 0.1)

        self.assertEqual(discountComposite.getDiscountId(), 5)
        self.assertEqual(discountComposite.getDiscount1(), 0)
        self.assertEqual(discountComposite.getDiscount2(), 1)
        self.assertEqual(discountComposite.getDiscountType(), 'Max')





if __name__ == '__main__':
    unittest.main()
