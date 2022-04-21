from interface import Interface

class IMarket(Interface):
    def addGuest(self):
        pass

    def checkOnlineMember(self, userName):
        pass

    def getStoreByName(self, store_name):
        pass

    def getStoreById(self, id_store):
        pass

    def getProductByCatagory(self, catagory):
        pass

    def getProductsByName(self, nameProduct):
        pass

    def getProductByKeyWord(self, keyword):
        pass

    def getUserByName(self, userName):
        pass

    def createStore(self, storeName, userID, bank, address):
        pass

    def addProductToCart(self, userID, storeID, product, quantity):
        pass

    def getStoreHistory(self, userName, storeID):
        pass

    def removeProductFromCart(self, userID, storeID, product):
        pass

    def updateProductFromCart(self, userID, storeID, product, quantity):
        pass

    def ChangeProductQuanInCart(self, userID, storeID, product, quantity):
        pass

    def appointManagerToStore(self, storeID, assignerID, assigneID):
        pass

    def appointOwnerToStore(self, storeID, assignerID, assigneID):
        pass

    def setStockManagerPermission(self, storeID, assignerID, assigneID):
        pass

    def setAppointOwnerPermission(self, storeID, assignerID, assigneID):
        pass

    def setChangePermission(self, storeID, assignerID, assigneID):
        pass

    def setRolesInformationPermission(self, storeID, assignerID, assigneID):
        pass

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneID):
        pass

    def addProductToStore(self, storeID, userID, product):
        pass

    def addProductQuantityToStore(self, storeID, userID, product, quantity):
        pass

    def removeProductFromStore(self, storeID, userID, product):
        pass

    def PrintRolesInformation(self, storeID, userID):
        pass

    def addTransaction(self, storeID, transaction):
        pass

    def removeTransaction(self, storeID, transaction):
        pass

    def printPurchaseHistoryInformation(self, storeID, userID):
        pass

    def updateProductFromStore(self, userID, productId, newProduct):
        pass


    def removeBag(self, storeID, userID):
        pass

    def updateBag(self, bag, userID):
        pass

    def getAllProducts(self, userID):
        pass

    def isEmpty(self, userID):
        pass

    def calcSum(self, userID):
        pass

