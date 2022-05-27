import unittest
import os, django

from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Product import Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from Backend.Business.Rules.PriceRule import PriceRule


class MyTestCase(unittest.TestCase):
    def test_rule_getters(self):
        rule_price = PriceRule(0, 'Store', None, 200, 1000, 'Discount')
        self.assertEqual(rule_price.getRuleId(), 0)
        self.assertEqual(rule_price.getRuleKind(), 'Discount')

    def test_rule_bag(self):
        rule_price = PriceRule(0, 'Store', None, 200, 1000, 'Discount')
        bag = Bag(0)
        product = Product(0, 0, "Test", 50, "Category", 5, [])
        bag.addProduct(product.getModel(), 6)
        self.assertEqual(rule_price.check(bag), True)


if __name__ == '__main__':
    unittest.main()
