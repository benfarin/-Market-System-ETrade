from zope.interface import Interface


class IBag(Interface):

    def isEmpty(self):
        pass

    def getStoreId(self):
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

    def cleanBag(self):
        pass

    def printProducts(self):
        pass

    def addBag(self, bag):
        pass

