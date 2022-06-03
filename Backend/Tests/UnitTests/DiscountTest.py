import unittest

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount
from Backend.Business.Rules.PriceRule import PriceRule
from Backend.Business.Rules.PurchaseRuleComposite import PurchaseRuleComposite
from Backend.Business.Rules.QuantityRule import quantityRule
from Backend.Business.Rules.WeightRule import weightRule
from ModelsBackend.models import DiscountRulesModel


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.discountCategory = CategoryDiscount(0, "Electric", 0.5)
        self.discountProduct = ProductDiscount(1, 0, 0.85)
        self.discountStore = StoreDiscount(3, 0.1)
        self.discountComposite = DiscountComposite(5, self.discountCategory, self.discountProduct, 'Max')

        self.rule1 = PriceRule(0, 'Store', None, 200, 1000, 'Discount')
        self.rule2 = quantityRule(1, 'Product', 1, 0, 1000, 'Discount')

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

    def test_rule_in_discount(self):
        self.discountCategory.addSimpleRuleDiscount(self.rule1)
        self.discountCategory.addSimpleRuleDiscount(self.rule2)
        self.rule3 = self.discountCategory.addCompositeRuleDiscount(3, self.rule1.getRuleId(), self.rule2.getRuleId(),
                                                                    'Max', 'Discount')
        self.discountCategory.removeDiscountRule(self.rule3.getRuleId())

        dis = DiscountRulesModel.objects.filter(discountID=self.discountCategory.getModel(),
                                                ruleID=self.rule3.getModel())
        self.assertEqual(0, len(dis))

        self.discountProduct.addSimpleRuleDiscount(self.rule1)
        self.discountProduct.addSimpleRuleDiscount(self.rule2)
        self.rule3 = self.discountProduct.addCompositeRuleDiscount(3, self.rule1.getRuleId(), self.rule2.getRuleId(),
                                                                    'Max', 'Discount')
        self.discountProduct.removeDiscountRule(self.rule3.getRuleId())

        dis = DiscountRulesModel.objects.filter(discountID=self.discountProduct.getModel(),
                                                ruleID=self.rule3.getModel())
        self.assertEqual(0, len(dis))

        self.discountStore.addSimpleRuleDiscount(self.rule1)
        self.discountStore.addSimpleRuleDiscount(self.rule2)
        self.rule3 = self.discountStore.addCompositeRuleDiscount(3, self.rule1.getRuleId(), self.rule2.getRuleId(),
                                                                    'Max', 'Discount')
        self.discountStore.removeDiscountRule(self.rule3.getRuleId())

        dis = DiscountRulesModel.objects.filter(discountID=self.discountStore.getModel(),
                                                ruleID=self.rule3.getModel())
        self.assertEqual(0, len(dis))

    def tearDown(self):
        self.rule1.removeRule()
        self.rule2.removeRule()
        self.discountCategory.remove()
        self.discountComposite.remove()
        self.discountProduct.remove()
        self.discountStore.remove()


if __name__ == '__main__':
    unittest.main()
