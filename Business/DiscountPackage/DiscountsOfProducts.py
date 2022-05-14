from typing import Dict


class DiscountOfProducts: #wad created by interface IDiscount.represent the products of some bag  hold Dict of the product's bag <productid, price> the price calculated by the percent it got  .in addition the object hold the discount (at least one of) the products got

    def __init__(self):
        self.__products: Dict[int, float] = {} #<pid,price>
        self.__discount = 0

    def getDiscount(self):
        return self.__discount

    def addProduct(self, pid, price):
        self.__products[pid] = price

    def increaseDiscount(self, discount):
        self.__discount += discount

    def addDiscount(self, products_discount, products_to_add):
        to_return = DiscountOfProducts()
        to_return.increaseDiscount(products_discount)
        for key, value in self.__products.items():
            to_return.__products[key] = value+products_to_add[key]
        return to_return

    def getProducts(self):
        return self.__products

    def setDiscount(self, discount):
        self.__discount = discount

