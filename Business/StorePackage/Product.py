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

    def getProductCategory(self):
        return self.__category

    def setProductName(self, name):
        self.__name = name

    def setProductPrice(self, price):
        self.__price = price

    def setProductCategory(self, category):
        self.__category = category

    def printForEvents(self):
        productStr = "\n\t\t\tid: " + str(self.__id)
        productStr += "\n\t\t\tname: " + self.__name
        productStr += "\n\t\t\tprice: " + str(self.__price)
        return productStr + "\n\t\t\tcategory: " + self.__category



