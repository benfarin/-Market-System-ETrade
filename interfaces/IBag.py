from interface import Interface


class IBag(Interface):

    def isEmpty(self):
        pass

    def addProduct(self, product, quantity):
        pass

    def removeProduct(self, productId):
        pass

    def removeProductQuantity(self, product, quantity):
        pass

    def getProducts(self):
        pass

    def getProductQuantity(self, product):
        pass

    def calcSum(self):
        pass
