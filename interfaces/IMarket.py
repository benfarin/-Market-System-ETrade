from zope.interface import Interface


class IMarket(Interface):

    def getUserID(self):
        pass

    def createStore(self, storeName, user, bank, address):  # change test!
        pass

    def addProductToCart(self, user, storeID, productID, quantity):  # Tested
        pass

    def removeProductFromCart(self, storeID, user, productId):  # Tested
        pass

    def updateProductFromCart(self, user, storeID, productId, quantity):  # UnTested
        pass

    def getProductByCategory(self, category):
        pass

    def getProductsByName(self, nameProduct):
        pass

    def getProductByKeyWord(self, keyword):
        pass

    def getProductByPriceRange(self, minPrice, highPrice):
        pass

    def addTransaction(self, storeID, transaction):
        pass

    def removeTransaction(self, storeID, transactionId):
        pass

    def purchaseCart(self, user, bank):
        pass

    def appointManagerToStore(self, storeID, assigner, assignee):  # Tested
        pass

    def appointOwnerToStore(self, storeID, assigner, assignee):  # unTested
        pass

    def setStockManagerPermission(self, storeID, assigner, assignee):  # Tested
        pass

    def setAppointOwnerPermission(self, storeID, assigner, assignee):  # Tested
        pass

    def setChangePermission(self, storeID, assigner, assignee):
        pass

    def setRolesInformationPermission(self, storeID, assigner, assignee):
        pass

    def setPurchaseHistoryInformationPermission(self, storeID, assigner, assignee):
        pass

    def addProductToStore(self, storeID, user, product):  # Tested
        pass

    def updateProductPrice(self, storeID, user, productId, mewPrice):
        pass

    def addProductQuantityToStore(self, storeID, user, productId, quantity):
        pass

    def removeProductFromStore(self, storeID, user, productId):
        pass

    def getRolesInformation(self, storeID, user):
        pass

    def getPurchaseHistoryInformation(self, storeID, user):
        pass

    def getStoreByName(self, store_name):
        pass

    def getStoreById(self, id_store):  # maybe should be private
        pass

    def getUserByName(self, userName):
        pass

    def getStores(self):
        pass

    # need to add to the service
    def removeStore(self, storeID, user):
        pass

    def loginUpdates(self, user):
        pass

    def updateProductName(self, user, storeID, productID, newName):
        pass

    def updateProductCategory(self, user, storeID, productID, newCategory):
        pass

    def addProductToCartWithoutStore(self, user, productID, quantity):
        pass