from zope.interface import Interface


class IMember(Interface):

    def getMemberName(self):
        pass

    def createStore(self, storeName, bank, address):
        pass

    def removeStore(self, storeId, user):
        pass

    def getMemberTransactions(self):
        pass

    def appointManagerToStore(self, storeID, assignee):
        pass

    def appointOwnerToStore(self, storeID, assignee):
        pass

    def setStockManagerPermission(self, storeID, assignee):
        pass

    def setAppointOwnerPermission(self, storeID, assignee):
        pass

    def setChangePermission(self, storeID, assignee):
        pass

    def setRolesInformationPermission(self, storeID, assignee):
        pass

    def setPurchaseHistoryInformationPermission(self, storeID, assignee):
        pass

    def setDiscountPermission(self, storeID, assignee):
        pass

    def addProductToStore(self, storeID, product):
        pass

    def addProductQuantityToStore(self, storeID, productId, quantity):
        pass

    def removeProductFromStore(self, storeID, product):
        pass

    def updateProductPrice(self, storeID, productId, newPrice):
        pass

    def updateProductName(self, storeID, productID, newName):
        pass

    def updateProductCategory(self, storeID, productID, newCategory):
        pass

    def updateProductWeight(storeID, productID, newWeight):
        pass

    def getRolesInformation(self, storeID):
        pass

    def getPurchaseHistoryInformation(self, storeID):
        pass

    def removeStoreOwner(self, storeId, assignee):
        pass

    def addDiscount(self, storeId, discount):
        pass

    def removeDiscount(self, storeId, discountId):
        pass

    def addConditionDiscountAdd(self, storeId, dId, dId1, dId2):
        pass

    def addConditionDiscountMax(self, storeId, dId, dId1, dId2):
        pass

    def updateCart(self, cart):
        pass

    def hasRole(self):
        pass

    def addConditionDiscountOr(self, storeId, discountId, dId, pred1, pred2):
        pass

    def addConditionDiscountAnd(self, storeId, discountId, dId, pred1, pred2):
        pass

    def addConditionDiscountXor(self, storeId, discountId, dId, pred1, pred2):
        pass


