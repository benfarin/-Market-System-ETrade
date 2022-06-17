from zope.interface import Interface


class IMarket(Interface):

    def getUserID(self):
        pass

    def isStoreExists(self, storeId):
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

    def purchaseCart(self, user, cardNumber, month, year, holderCardName, cvv, holderID, address):
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

    def setDiscountPermission(self, storeID, assigner, assignee):
        pass

    def addProductToStore(self, storeID, user, product):  # Tested
        pass

    def updateProductPrice(self, user, StoreId, productId, mewPrice):
        pass

    def updateProductWeight(self, user, storeID, productID, newWeight):
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

    def getUserStores(self, user):
        pass

    def removeStoreOwner(self, storeID, assigner, assignee):
        pass

    def hasRole(self, user):
        pass

    def getAllStoreTransactions(self):
        pass

    def getAllUserTransactions(self):
        pass

    def getStoreTransaction(self, transactionId):
        pass

    def getUserTransaction(self, transactionId):
        pass

    def getStoreTransactionByStoreId(self, storeId):
        pass

    def recreateStore(self, storeID, founder):
        pass

    def removeStoreForGood(self, storeId, founder):
        pass

    def updateCart(self, cart1, cart2):
        pass

    def addSimpleDiscount(self, user, storeId, discount):
        pass

    def addCompositeDiscount(self, user, storeId, discountId, dId1, dId2, typeDiscount, decide):
        pass

    def removeDiscount(self, user, storeId, discountId):
        pass

    def addSimpleRule(self, user, storeId, dId, rule):
        pass

    def addCompositeRule(self, user, storeId, dId, ruleId, rId1, rId2, ruleType, ruleKind):
        pass

    def removeRule(self, user, storeId, dId, rId, ruleKind):
        pass

    def getCartSum(self, user):
        pass

    def getAllDiscountOfStore(self, user, storeId, isComp):
        pass

    def getAllPurchaseRulesOfStore(self, user, storeId, isComp):
        pass

    def getAllRulesOfDiscount(self, user, storeId, discountId, isComp):
        pass

    def getCheckNoOwnerYesManage(self, user):
        pass

    def getCheckNoOwnerNoManage(self, user):
        pass

    def getCheckOwner(self, user):
        pass

    def openNewBidOffer(self, user, storeID, productID, newPrice):
        pass

    def acceptBidOffer(self, user, storeID, bID):
        pass

    def rejectOffer(self, storeID, bID):
        pass

    def offerAlternatePrice(self, user, storeID, bID, new_price):
        pass

    def changeExternalPayment(self, paymentSystem):
        pass

    def changeExternalDelivery(self, deliverySystem):
        pass

    def acceptOwnerAgreement(self, user, storeID, ownerAcceptID):
        pass

    def rejectOwnerAgreement(self, storeID, ownerAcceptID):
        pass

    def getBid(self, storeId, bid):
        pass

    def getAllStoreBids(self, storeId):
        pass

    def getOwnerAgreementById(self, storeId, oaId):
        pass

    def getAllStoreOwnerAgreements(self, storeId):
        pass
