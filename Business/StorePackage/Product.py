class Product:

    def __init__(self, Id, name, price, category):
        self.__id = Id
        self.__name = name
        self.__price = price
        self.__category = category  # String

    def getProductId(self):
        return self.__id

    def getProductName(self):
        return self.__name

    def getProductPrice(self):
        return self.__price

    def setProductPrice(self, price):
        self.__price = price

    def getProductCategory(self):
        return self.__category


