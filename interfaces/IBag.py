from interface import Interface


class IBag(Interface):

    def isEmpty(self):
        pass

    def addProduct(self, product, quantity):
        pass

    def removeProduct(self, productId):
        pass

    def updateProduct(self, productId, quantity):
        pass

    def getProducts(self):
        pass

    def getProductQuantity(self, product):
        pass

    def calcSum(self):
        pass
