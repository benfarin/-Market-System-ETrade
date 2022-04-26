from interface import Interface


class IStore(Interface):

    def getStoreId(self):
        pass

    def getStoreFounderId(self):
        pass

    def getStoreBankAccount(self):
        pass

    def getStoreAddress(self):
        pass

    def getStoreOwners(self):
        pass

    def getStoreManagers(self):
        pass

    def getProducts(self):
        pass

    def getProductQuantity(self):
        pass

    def setStockManagementPermission(self, assignerId, assigneeId):
        pass

    def setAppointManagerPermission(self, assignerId, assigneeId):
        pass

    def setAppointOwnerPermission(self, assignerId, assigneeId):
        pass

    def setChangePermission(self, assignerId, assigneeId):
        pass

    def setRolesInformationPermission(self, assignerId, assigneeId):
        pass

    def setPurchaseHistoryInformationPermission(self, assignerId, assigneeId):
        pass

    def addProductToStore(self, userId, product):
        pass

    def addProductQuantityToStore(self, userId, productId, quantity):
        pass

    def removeProductFromStore(self, userId, productId):
        pass

    def updateProductFromStore(self, userId, productId, newProduct):
        pass

    def appointManagerToStore(self, assignerId, assigneeId):
        pass

    def appointOwnerToStore(self, assignerId, assigneeId):
        pass

    def PrintRolesInformation(self, userId):
        pass

    def getPermissions(self, userId):
        pass

    def addTransaction(self, transaction):
        pass

    def removeTransaction(self, transactionId):
        pass

    def getTransaction(self, transactionId):
        pass

    def printPurchaseHistoryInformation(self, userId):
        pass

    def getTransactionHistory(self, userId):
        pass

    def getProductsByName(self, productName):
        pass

    def getProductsByKeyword(self, keyword):
        pass

    def getProductsByCategory(self, productCategory):
        pass

    def getProductsByPriceRange(self, minPrice, maxPrice):
        pass

    def addProductToBag(self, productId, quantity):
        pass

    def removeProductFromBag(self, productId, quantity):
        pass

    def updateProductName(self,userId ,productID, newName):
        pass

    def updateProductCategory(self,userId ,productID, newCategory):
        pass