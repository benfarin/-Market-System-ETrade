from interface import Interface

from Business.UserPackage.User import User


class IMarket(Interface):
    def addGuest(self):
        pass

    def getStoreByName(self, store_name):
        pass

    def getStoreById(self, id_store):
        pass

    def getProductByCategory(self, category):
        pass

    def getProductsByName(self, nameProduct):
        pass

    def getProductByKeyWord(self, keyword):
        pass

    def getUserByName(self, userName):
        pass

    def createStore(self, storeName, userID, bank, address):
        pass

    def addProductToCart(self, userID, storeID, productID, quantity):
        pass

    def removeProductFromCart(self,storeID ,userID, productId):
        pass

    def updateProductFromCart(self, userID, storeID, productId, quantity):
        pass

    def appointManagerToStore(self, storeID, assignerID, assigneeID):
        pass

    def appointOwnerToStore(self, storeID, assignerID, assigneeID):
        pass

    def setStockManagerPermission(self, storeID, assignerID, assigneeID):
        pass

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID):
        pass

    def setChangePermission(self, storeID, assignerID, assigneeID):
        pass

    def setRolesInformationPermission(self, storeID, assignerID, assigneeID):
        pass

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        pass

    def addProductToStore(self, storeID, userID, product):
        pass

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        pass

    def removeProductFromStore(self, storeID, userID, productId):
        pass

    def printRolesInformation(self, storeID, userID):
        pass

    def addTransaction(self, storeID, transaction):
        pass

    def removeTransaction(self, storeID, transactionId):
        pass

    def printPurchaseHistoryInformation(self, storeID, userID):
        pass

    def updateProductPrice(self, storeID, userID, productId, mewPrice):
        pass

    def addActiveUser(self, user):
        pass

    def purchaseCart(self, userID, bank):
        pass

    def loginUpdates(self, userID):
        pass

    def removeStore(self, storeID, userID):
        pass

    def getCart(self, userID):
        pass

