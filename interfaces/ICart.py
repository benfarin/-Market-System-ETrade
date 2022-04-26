from interface import Interface


class ICart(Interface):

    def getUserId(self):
        pass

    def getAllBags(self):
        pass

    def getBag(self, storeId):
        pass

    def removeBag(self, storeId):
        pass

    def updateBag(self, bag):
        pass

    def calcSum(self):
        pass

    def isEmpty(self):
        pass

    def addProduct(self, storeId, product, quantity):
        pass

    def removeProduct(self, storeId, productId):
        pass

    def updateProduct(self, storeId, productId, quantity):  # quantity can be negative!!!
        pass

    def cleanCart(self):
        pass

    def printBags(self):
        pass
