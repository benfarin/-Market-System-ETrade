class DiscountInfo:

    def __init__(self, id_discount, user_id, id_store, rule_contex, rule_type, percent, category, product_id,
                value_less_than,value_grather_than, time1, time2):

        self.__id_discount = id_discount
        self.__user_id = user_id
        self.__id_store = id_store
        self.__discount_type = rule_contex
        self.__rule_type = rule_type
        self.__percent = percent
        self.__category = category
        self.__product_id = product_id
        self.__value_less_than = value_less_than
        self.__value_grather_than = value_grather_than
        self.__time1 = time1
        self._time2 = time2

    def getIdDiscount(self):
        return self.__id_discount

    def getStoreID(self):
        return  self.__id_store

