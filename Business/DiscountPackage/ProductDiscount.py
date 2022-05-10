from interfaces import IDiscount
from Business.StorePackage import  Bag,Product
from typing import Dict
from Business.DiscountPackage import DiscountCalc, DiscountsOfProducts


class ProductDiscount(IDiscount):

    def __int__(self, product_ID, percent):
        self.__F = lambda a: self.calculate(a, product_ID, percent)
        self.__discountCalc: DiscountCalc = DiscountCalc(self.__F)

    def calculate(self, bag: Bag, product_ID, percent):
        to_return = DiscountsOfProducts()
        discount = 0
        products: Dict[Product, int] = bag.getProducts()
        for prod, quantity in products.items():
            if prod.getProductId() == product_ID:
                discount += quantity*prod.getProductPrice()*percent
                to_return.addProduct(prod.getProductId(), (1-percent)*prod.getProductPrice())
            else:
                to_return.addProduct(prod.getProductId(), prod.getProductPrice())
            to_return.setDiscount(discount)
            return to_return

    def calcDiscount(self, bag):
        return self.__discountCalc.calcDiscount(bag)

    def max(self, additional_DiscountCal):
        return self.__discountCalc.max(additional_DiscountCal)

    def add(self, discount_calc_2):
        return self.__discountCalc.add(discount_calc_2)






