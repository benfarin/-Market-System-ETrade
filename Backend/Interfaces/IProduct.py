from zope.interface import Interface


class IProduct(Interface):

    def getProductId(self):
        pass

    def getProductName(self):
        pass

    def getProductPrice(self):
        pass

    def getProductCategory(self):
        pass

    def setProductName(self, name):
        pass

    def setProductCategory(self, category):
        pass

    def setProductPrice(self, price):
        pass

    def addKeyWord(self, keyword):
       pass

    def removeKeyWord(self, keyword):
        pass

    def isExistsKeyword(self, keyword):
        pass

    def printForEvents(self):
        pass
