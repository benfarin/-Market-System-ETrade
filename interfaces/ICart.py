from interface import Interface


class ICart(Interface):

    def isEmpty(self):
        pass

    def getAllBags(self):
        pass

    def getBag(self, bagId):
        pass

    def addBag(self, storeId, bag):
        pass

    def removeBag(self, bagId):
        pass

    def updateBag(self, bag):
        pass

    def calcSum(self):
        pass

    def getAllProduct(self):
        pass