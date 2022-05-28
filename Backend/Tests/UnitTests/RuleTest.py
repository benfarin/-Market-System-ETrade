import unittest
import os, django

from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Product import Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from Backend.Business.Rules.PriceRule import PriceRule


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.rule_price = PriceRule(0, 'Store', None, 200, 1000, 'Discount')
        self.bag = Bag(0, 0)
        self.product = Product(0, 0, "Test", 50, "Category", 5, [])

    def test_rule_getters(self):
        self.assertEqual(self.rule_price.getRuleId(), 0)
        self.assertEqual(self.rule_price.getRuleKind(), 'Discount')

    def test_rule_bag(self):
        self.bag.addProduct(self.product.getModel(), 6)
        self.assertEqual(self.rule_price.check(self.bag), True)

    def tearDown(self):
        self.rule_price.removeRule()
        self.bag.removeBag()
        self.product.removeProduct()


if __name__ == '__main__':
    unittest.main()
