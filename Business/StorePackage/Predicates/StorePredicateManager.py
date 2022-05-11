from Business.DiscountPackage.Discount import Discount
from typing import Dict
class storePredicateManager:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if storePredicateManager.__instance is None:
            storePredicateManager()
        return storePredicateManager.__instance

    def __init__(self):
        self.__discount_store = {}    #[id_store,[] Discount]
        self.__store_policies = {}  #implement next by kfir
        if storePredicateManager.__instance is None:
            Market.__instance = self

    def addDiscount(self, id_store, discount : Discount):
        if self.__discount_store.get(id_store) is not None:
            self.__discount_store.get(id_store).add(discount)
        else:
            self.__discount_store[id_store] = set()
            self.__discount_store.get(id_store).add(discount)

    def getDiscountsByIdStore(self, id_store):
        return self.__discount_store.get(id_store)  # if its empty will return None

    def getSingleDiscountByID(self, id_store, id_discount):
        discounts =  self.__discount_store.get(id_store)
        if discounts is not None :
            for discount in discounts:
                if discount.getIdDiscount() == id_discount:
                    return discount
        return None









