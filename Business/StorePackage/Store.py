from interface import implements
from interfaces import IStore
from Business.StorePackage.StorePermission import StorePermission
from typing import Dict, List


class Store(implements(IStore)):

    def __init__(self, storeId, storeName, founderId):
        # need to add address and bank account
        self.__id = storeId
        self.__name = storeName
        self.__rating = 0
        self.__numOfRatings = 0
        self.__founderId = founderId
        self.__appointers: Dict[int, List] = {}  # UserId : UserId list
        self.__managers = []  # userId
        self.__owners = []  # userId
        self.__products = {}  # productId : Product
        self.__transactions = {}  # transactionId : Transaction

        self.__permissions = {founderId: StorePermission()}  # UserId : storePermission
        self.__permissions[founderId].setPermission_AppointManager(True)
        self.__permissions[founderId].setPermission_AppointOwner(True)
        self.__permissions[founderId].setPermission_CloseStore(True)

    def getStoreId(self):
        return self.__id

    def getStoreFounderId(self):
        return self.__founderId

    def getStoreOwners(self):
        return self.__owners

    def getStoreManagers(self):
        return self.__managers

    def setStockManagementPermission(self, assignerId, assigneeId):
        try:
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_ChangePermission(True)
        except Exception as e:
            raise Exception(e)

    def setAppointManagerPermission(self, assignerId, assigneeId):
        try:
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_AppointManager(True)
        except Exception as e:
            raise Exception(e)

    def setAppointOwnerPermission(self, assignerId, assigneeId):
        try:
            self.__haveAllPermissions(assignerId, assigneeId)
            if assignerId not in self.__owners:
                raise Exception("only owners can assign owners")
            self.__permissions[assigneeId].setPermission_AppointOwner(True)
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, assignerId, assigneeId):
        try:
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_ChangePermission(True)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, assignerId, assigneeId):
        try:
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_RolesInformation(True)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, assignerId, assigneeId):
        try:
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_PurchaseHistoryInformation(True)
        except Exception as e:
            raise Exception(e)

    def __haveAllPermissions(self, assignerId, assigneeId):
        # next version need to add parameter for removing.
        permissions = self.__permissions[assignerId]
        if permissions is None:
            raise Exception("User ", assignerId, " doesn't have any permissions is store:", self.__id)
        if not permissions.hasPermission_ChangePermission():
            raise Exception("User ", assignerId, "cannot change permission in store: ", self.__id)
        if assigneeId not in self.__appointers[assignerId]:
            raise Exception("User ", assignerId, "cannot change the permissions of user: ", assigneeId,
                            " because he didn't assign him")

    def addProduct(self, userId, product):
        try:
            self.__checkPermissions_ChangeStock(userId, "add product")
            self.__products[product.getProductId()] = product
        except Exception as e:
            raise Exception(e)

    def removeProduct(self, userId, productId):
        try:
            self.__checkPermissions_ChangeStock(userId, "remove product")
            self.__products.pop(productId)
        except Exception as e:
            raise Exception(e)

    def updateProduct(self, userId, productId, newProduct):
        try:
            self.__checkPermissions_ChangeStock(userId, "update product")
            self.__products[productId] = newProduct
        except Exception as e:
            raise Exception(e)

    def __checkPermissions_ChangeStock(self, userId, line):
        permissions = self.__permissions[userId]
        if permissions is None:
            raise Exception("User ", userId, " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_StockManagement():
            raise Exception("User ", userId, " doesn't have the permission - ", line, " in  store:", self.__name)

    def appointManagerToStore(self, assignerId, assigneeId):
        permissions = self.__permissions[assignerId]
        if permissions is None:
            raise Exception("User ", assignerId, " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_AppointManager():
            raise Exception("User ", assignerId, " doesn't have the permission - appoint manager in  store:",
                            self.__name)
        self.__managers.append(assigneeId)
        self.__appointers[assigneeId].append(assigneeId)
        self.__permissions[assigneeId] = StorePermission()

    def appointOwnerToStore(self, assignerId, assigneeId):
        permissions = self.__permissions[assignerId]
        if permissions is None:
            raise Exception("User ", assignerId, " doesn't have any permissions is store:", self.__id)
        if not permissions.hasPermission_AppointOwner():
            raise Exception("User ", assignerId, " doesn't have the permission - appoint owner in  store:",
                            self.__name)
        self.__owners.append(assigneeId)
        self.__appointers[assignerId].append(assigneeId)

        ownerPermissions = StorePermission()
        ownerPermissions.setPermission_StockManagement(True)
        ownerPermissions.setPermission_AppointManager(True)
        ownerPermissions.setPermission_AppointOwner(True)
        ownerPermissions.setPermission_ChangePermission(True)
        ownerPermissions.setPermission_RolesInformation(True)
        ownerPermissions.setPermission_PurchaseHistoryInformation(True)
        self.__permissions[assigneeId] = ownerPermissions

    def addTransaction(self, transaction):
        pass

    def removeTransaction(self, transaction):
        pass

    def getStoreTransactionHistory(self):
        pass

    def editPermission(self, assignerId, assigneeId):
        pass

    def getProductsByName(self, productName):
        toReturnProducts = []
        for product in self.__products.keys():
            if product.getProductName() == productName:
                toReturnProducts.append(product)
        return toReturnProducts

    def getProductsByKeyword(self, productName):
        pass

    def getProductsByCategory(self, productCategory):
        toReturnProducts = []
        for product in self.__products.keys():
            if product.getProductCategory() == productCategory:
                toReturnProducts.append(product)
        return toReturnProducts

    def getProductsByPriceRange(self, minPrice, maxPrice):
        toReturnProducts = []
        for product in self.__products.keys():
            price = product.getProductPrice()
            if minPrice <= price <= maxPrice:
                toReturnProducts.append(product)
        return toReturnProducts

    def getProductsByMinRating(self, minRating):
        toReturnProducts = []
        for product in self.__products.keys():
            if minRating <= product.getProductRating():
                toReturnProducts.append(product)
        return toReturnProducts

    def getProductRating(self, productId):
        self.__products[productId].getProductRating()

    def setProductRating(self, productId, rating):
        self.__products[productId].getProductRating(rating)

    def getStoreRating(self):
        return self.__rating

    def setStoreRating(self, rating):
        if rating <= 0 or rating >= 5:
            raise Exception("not a valid rating")
        self.__rating = (self.__numOfRatings * self.__rating + rating) / (self.__numOfRatings + 1)
        self.__numOfRatings += 1
