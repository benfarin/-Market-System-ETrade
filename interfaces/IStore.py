from interface import Interface


class IStore(Interface):

    def getStoreId(self):
        pass

    def getStoreFounderId(self):
        pass

    def getStoreOwners(self):
        pass

    def getStoreManagers(self):
        pass

    def addProduct(self, userId, product):
        pass

    def removeProduct(self, userId, productId):
        pass

    def updateProduct(self, userId, productId, newProduct):
        pass

    def addTransaction(self, transaction):
        pass

    def removeTransaction(self, transaction):
        pass

    def getStoreTransactionHistory(self):
        pass

    def getProductsByName(self, productName):
        pass

    def getProductsByKeyword(self, productName):
        pass

    def getProductsByCategory(self, productCategory):
        pass

    def getProductsByPriceRange(self, minPrice, maxPrice):
        pass

    def getProductsByMinRating(self, minRating):
        pass

    def addProductToBag(self, productId, quantity):
        pass

    def removeProductFromBag(self, productId, quantity):
        pass

    def appointManagerToStore(self, assignerId, assigneeId):
        pass

    def appointOwnerToStore(self, assignerId, assigneeId):
        pass