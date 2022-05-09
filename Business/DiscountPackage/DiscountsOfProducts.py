from typing import Dict


class DiscountOfProducts:

    def __int__(self):
        self.__products : Dict[int,float] = {}
        self.__discount = 0

    def addProduct(self, pid, price):
        self.__products[pid] = price

    def increaseDiscount(self, discount):
        self.__discount += discount

    def addDiscount(self, products_discount, products_to_add):
        to_return: DiscountOfProducts
        to_return.increaseDiscount(products_discount)
        for key, value in self.__products:
            to_return.__products[key]= value+products_to_add[key]
        return  to_return