import zope

from Backend.Interfaces.IDiscount import IDiscount
from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Product import Product
from typing import Dict
from Backend.Business.DiscountPackage.DiscountCalc import DiscountCalc
from Backend.Business.DiscountPackage.DiscountsOfProducts import DiscountOfProducts


@zope.interface.implementer(IDiscount)
class ProductDiscount:

    def __init__(self, product_ID, percent):
        self.__F = lambda bag: self.calculate(bag, product_ID, percent)
        self.__discountCalc: DiscountCalc = DiscountCalc(self.__F)

    def calculate(self, bag: Bag, product_ID, percent): # each of the products got an percent from the owner of the store, this function get bag and check over it if this product in his bag , the function return an object ProductOfDiscount which contain Dict <product_id, price> all of the products and their price calculated after the discount this specific product brought.
        to_return = DiscountOfProducts()
        # discount = 0
        products: Dict[Product, int] = bag.getProducts()
        for prod, quantity in products.items():
            if prod.getProductId() == product_ID:
                # discount += percent
                to_return.addProduct(prod, (1-percent))
            else:
                to_return.addProduct(prod, 1.0)
            # to_return.setDiscount(discount)
        return to_return

    def calcDiscount(self, bag):
        return self.__discountCalc.calcDiscount(bag)

    def max(self, additional_DiscountCal):
        return self.__discountCalc.max(additional_DiscountCal)

    def add(self, discount_calc_2):
        return self.__discountCalc.adxd(discount_calc_2)






