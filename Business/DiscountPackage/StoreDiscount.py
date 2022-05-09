from interfaces import IDiscount
from Business.StorePackage import  Bag,Product
from typing import Dict
from Business.DiscountPackage import DiscountCalc,DiscountsOfProducts
class StoreDiscount(IDiscount):

    def __int__(self, percent):
        self.F = lambda a : self.calculate(a, percent)
        self.discountCalc :DiscountCalc = DiscountCalc(self.F)

    def calculate(self, bag: Bag, percent):
        to_return = DiscountsOfProducts()
        discount = 0
        products: Dict[Product, int] = bag.getProducts()
        for prod, quantity in products.items():
            self.discountCalc += quantity*prod.getProductPrice()*percent
