import datetime


class Transaction:

    def __init__(self, userId, storeId, products, amount):
        self.__userId = userId
        self.__storeId = storeId
        self.__date = datetime.datetime.now().strftime("%x") + datetime.datetime.now().strftime("%X")
        self.__products = products
        self.__amount = amount
