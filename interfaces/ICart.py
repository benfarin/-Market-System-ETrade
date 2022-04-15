from interface import Interface


class ICart(Interface):

    def getUserId(self):
        pass

    def isEmpty(self):
        pass

    def getAllBags(self):
        pass

    def getBag(self, storeId):
        pass

    def addBag(self, storeId):
        pass

    def removeBag(self, storeId):
        pass

    def updateBag(self, bag):
        pass

    def calcSum(self):
        pass

    def getAllProduct(self):
        pass