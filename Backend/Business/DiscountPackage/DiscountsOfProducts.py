from typing import Dict

from Backend.Business.StorePackage.Product import Product


class DiscountOfProducts:  # wad created by interface IDiscount.represent the products of some bag  hold Dict of the product's bag <productid, price> the price calculated by the percent it got  .in addition the object hold the discount (at least one of) the products got

    def __init__(self):
        self.__products: Dict[Product, float] = {}  # <product, discount>
        # self.__discount = 0

    # def getDiscount(self):
    #     return self.__discount

    def getTotalDiscountPrice(self):
        s = 0.0
        for prod in self.__products.keys():
            s += prod.getProductPrice() * self.__products[prod]
        return s

    def addProduct(self, product, discount):
        self.__products[product] = discount

    # def increaseDiscount(self, discount):
    #     self.__discount += discount
    #     self.__discount = 1 - ((1-discount) + (1-self.__discount))

    def addDiscount(self, products_to_add):
        to_return = DiscountOfProducts()
        # to_return.setDiscount(self.__discount)
        to_return.setProducts(self.__products)
        # to_return.increaseDiscount(products_discount)
        for key, value in self.__products.items():
            to_return.__products[key] = 1 - ((1-value) + (1 - products_to_add[key]))
        return to_return

    def getProducts(self):
        return self.__products

    # def setDiscount(self, discount):
    #     self.__discount = discount

    def setProducts(self, products):
        self.__products = products

    def getProductPrice(self, pid):
        return self.__products.get(pid)
