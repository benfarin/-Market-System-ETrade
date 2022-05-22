from zope.interface import Interface


class IStore(Interface):

    def getStoreId(self):
        pass

    def getProduct(self, productId):
        pass

    def hasProduct(self, productId):
        pass

    def setStockManagementPermission(self, assigner, assignee):
        pass

    def setAppointManagerPermission(self, assigner, assignee):
        pass

    def setAppointOwnerPermission(self, assigner, assignee):
        pass

    def setChangePermission(self, assigner, assignee):
        pass

    def setRolesInformationPermission(self, assigner, assignee):
        pass

    def setPurchaseHistoryInformationPermission(self, assigner, assignee):
        pass

    def setDiscountPermission(self, assigner, assignee):
        pass

    def addProductToStore(self, user, product):
        pass

    def addProductQuantityToStore(self, user, productId, quantity):
        pass

    def removeProductFromStore(self, user, productId):
        pass

    def updateProductPrice(self, user, productId, newPrice):
        pass

    def updateProductName(self, user, productId, newName):
        pass

    def updateProductCategory(self, user, productId, newCategory):
        pass

    def updateProductWeight(self, user, productID, newWeight):
        pass

    def appointManagerToStore(self, assigner, assignee):
        pass

    def appointOwnerToStore(self, assigner, assignee):
        pass

    # print all permission in store - will be deleted this version
    def getRolesInformation(self, user):
        pass

    def getPermissions(self, user):
        pass

    def addTransaction(self, transaction):
        pass

    def removeTransaction(self, transactionId):
        pass

    def getTransaction(self, transactionId):
        pass

    # print all transactions in store - will be deleted in this version
    def getPurchaseHistoryInformation(self, user):
        pass

    def getTransactionHistory(self, user):
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

    def hasPermissions(self, user):
        pass

    def removeStoreOwner(self, assigner, assignee):
        pass

    def hasRole(self, user):
        pass

    def getTransactionsForSystemManager(self):
        pass

    def hasDiscountPermission(self, user):
        pass

    def addSimpleDiscount(self, user, discount):
        pass

    def addCompositeDiscount(self, user, discountId, dId1, dId2, discountType):
        pass

    def getAllDiscounts(self, user):
        pass

