from interfaces import IDiscount
from Business.StorePackage import  Bag,Product
from typing import Dict
from Business.DiscountPackage import DiscountCalc,DiscountsOfProducts
class ProductDiscount(IDiscount):

    def __int__(self,product_ID,percent):
        self.F = lambda a : self.calculate(a,product_ID,percent)
        self.discountCalc :DiscountCalc = DiscountCalc(self.F)

    def calculate(self, bag: Bag, product_ID, percent):
        to_return = DiscountsOfProducts()
        discount = 0
        products: Dict[Product, int] = bag.getProducts()
        for prod, quantity in products.items():
            if prod.getProductId() == product_ID:
                self.discountCalc += quantity*prod.getProductPrice()*percent
            else:







