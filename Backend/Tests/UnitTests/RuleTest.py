import unittest

from Backend.Business.Rules.PurchaseRuleComposite import PurchaseRuleComposite
from Backend.Business.Rules.QuantityRule import quantityRule
from Backend.Business.Rules.WeightRule import weightRule
from Backend.Business.Rules.PriceRule import PriceRule
from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Product import Product


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.rule_price = PriceRule(0, 'Store', None, 200, 1000, 'Discount')
        self.bag = Bag(0, 0)
        self.product = Product(0, 0, "Test", 50, "Category", 5, [])

    def test_rule_getters(self):
        self.assertEqual(self.rule_price.getRuleId(), 0)
        self.assertEqual(self.rule_price.getRuleKind(), 'Discount')

    def test_rule_bag(self):
        self.bag.addProduct(self.product, 6)
        self.assertEqual(self.rule_price.check(self.bag), True)

        self.bag.removeProduct(self.product.getProductId())

    def test_rule_composite(self):
        self.productRule = quantityRule(1, 'Product', 1, 0, 1000, 'Purchase')
        self.categoryRule = weightRule(2, 'Category', "Category", 0, 1000, 'Purchase')
        self.compRule = PurchaseRuleComposite(3, self.productRule, self.categoryRule, 'Or', 'Purchase')

        self.bag.addProduct(self.product, 10)
        self.assertEqual(500, self.bag.calcSum([]))

        self.productRule.removeRule()
        self.categoryRule.removeRule()
        self.compRule.removeRule()

    def tearDown(self):
        self.rule_price.removeRule()
        self.bag.removeBag()
        self.product.removeProduct()


if __name__ == '__main__':
    unittest.main()
