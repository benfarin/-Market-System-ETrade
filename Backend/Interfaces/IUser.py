from zope.interface import Interface


class IUser(Interface):

    def getUserID(self):
        pass

    def getCart(self):
        pass

    def addProductToCart(self, storeID, product, quantity):
        pass

    def removeProductFromCart(self, storeID, productId):
        pass

    def updateProductFromCart(self, storeID, productId, quantity):
        pass

    def purchaseCart(self, cardNumber, month, year, holderCardName, cvv, holderID, address):
        pass

    def getCartSum(self):
        pass

    def openNewBidOffer(self, storeID, productID, newPrice):
        pass

