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
        self.__discount_store: Dict[int: []] = {}  # [id_store,[] Discount]
        self.__store_policies = {}  # implement next by kfir
        if storePredicateManager.__instance is None:
            storePredicateManager.__instance = self

    def addDiscount(self, id_store, discount):
        if self.__discount_store.get(id_store) is not None:
            self.__discount_store[id_store] += 1 * [discount]
        else:
            self.__discount_store[id_store] = [discount]

    def getDiscountsByIdStore(self, id_store):
        return self.__discount_store.get(id_store)  # if its empty will return None

    def getSingleDiscountByID(self, id_store, id_discount):
        discounts = self.__discount_store.get(id_store)
        if discounts is not None:
            for discount in discounts:
                if id_discount == discount.getIdDiscount():
                    return discount
        return None

    def removeDiscount(self, sid, discount):
        if self.__discount_store.get(sid) is not None:
            lst = self.__discount_store.get(sid)
            for i in range(len(lst)):
                if lst[i] == discount:
                    self.__discount_store.get(sid).remove(discount)
                    break

