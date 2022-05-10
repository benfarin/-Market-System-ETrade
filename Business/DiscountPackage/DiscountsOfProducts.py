from typing import Dict


class DiscountOfProducts:

    def __init__(self):
        self.__products: Dict[int, float] = {}
        self.__discount = 0

    def getDiscount(self):
        return self.__discount

    def addProduct(self, pid, price):
        self.__products[pid] = price

    def increaseDiscount(self, discount):
        self.__discount += discount

    def addDiscount(self, products_discount, products_to_add):
        to_return: DiscountOfProducts
        to_return.increaseDiscount(products_discount)
        for key, value in self.__products.items():
            to_return.__products[key] = value+products_to_add[key]
        return to_return

    def getProducts(self):
        return self.__products

    def addProduct(self, key, value):
        self.__products[key] = value

    def setDiscount(self, discount):
        self.__discount = discount

