from interface import implements
from interfaces import ICart


class Cart(implements(ICart)):

    def __int__(self):
        self.__bags = dict()  # storeId : Bag

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

    def isEmpty(self):
        pass
