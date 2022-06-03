from Backend.Business.Rules.DiscountRuleComposite import DiscountRuleComposite
from Backend.Business.Rules.PriceRule import PriceRule
from Backend.Business.Rules.PurchaseRuleComposite import PurchaseRuleComposite
from Backend.Business.Rules.QuantityRule import quantityRule
from Backend.Business.Rules.WeightRule import weightRule


class RuleCreator:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if RuleCreator.__instance is None:
            RuleCreator()
        return RuleCreator.__instance

    def __init__(self):
        if RuleCreator.__instance is None:
            RuleCreator.__instance = self

    def buildRule(self, model):
        if model.rule_class == 'DiscountComposite':
            return DiscountRuleComposite(model=model)
        if model.rule_class == 'Price':
            return PriceRule(model=model)
        if model.rule_class == 'PurchaseComposite':
            return PurchaseRuleComposite(model=model)
        if model.rule_class == 'Quantity':
            return quantityRule(model=model)
        if model.rule_class == 'Weight':
            return weightRule(model=model)