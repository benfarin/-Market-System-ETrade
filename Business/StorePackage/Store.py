from interface import implements
from interfaces import IStore


class Store(implements(IStore)):

    def __init__(self, storeId, storeName, founderId):
        self.__id = storeId
        self.__name = storeName
        self.__rating = 0
        self.__numOfRating = 0
        self.__founderId = founderId
        self.__permissions = {}  # UserId : Permission
        self.__appointers = {int: []}  # UserId : UserId list
        self.__managers = []  # userId
        self.__owners = []  # userId
        self.__products = {}  # productId : Product
        self.__transactions = {}  # transactionId : Transaction

    def getStoreId(self):
        return self.__id

    def getStoreFounderId(self):
        return self.__founderId

    def getStoreOwners(self):
        return self.__owners

    def getStoreManagers(self):
        return self.__managers

    def addProduct(self, userId, product):
        try:
            self.__checkPermissions(userId, "add product")
            self.__products[product.getProductId()] = product
            return True
        except:
            return False

    def removeProduct(self, userId, productId):
        try:
            self.__checkPermissions(userId, "remove product")
            self.__products.pop(productId)
            return True
        except:
            return False

    def updateProduct(self, userId, productId, newProduct):
        try:
            self.__checkPermissions(userId, "update product")
            self.__products[productId] = newProduct
            return True
        except:
            return False

    def __checkPermissions_addProduct(self, userId, line):
        permissions = self.__permissions[userId]
        if permissions is None:
            raise Exception("User ", userId, " doesn't have any permissions is store:", self.__id)
        if not permissions.hasPremission_AddProduct():
            raise Exception("User ", userId, " doesn't have the permission - ", line, " in  store:", self.__id)

    def addRole(self, assignerId, assigneeId, role):
        permissions = self.__permissions[assignerId]
        if permissions is None:
            raise Exception("User ", assigneeId, " doesn't have any permissions is store:", self.__id)

        if role == 1:
            if not permissions.hasPremission_appointManager():
                raise Exception("User ", assigneeId, " doesn't have the permission - appoint manager in  store:",
                                self.__id)
            self.__appointers[assignerId].append([assigneeId])
            self.__managers.append([assigneeId])
            # here assignee need to get some of the permissions of a manager

        elif role == 2:
            if not permissions.hasPremission_appointOwner():
                raise Exception("User ", assigneeId, " doesn't have the permission - appoint owner in  store:",
                                self.__id)
            self.__appointers[assignerId].append([assigneeId])
            self.__owners.append([assigneeId])
            # here assignee need to get some of the permissions of a manager

        else:
            raise Exception("no such role")

    def removeRole(self, assignerId, assigneeId, role):
        if assigneeId not in self.__appointers[assignerId]:
            raise Exception("only the one how assign can remove")
        if role == 1:
            self.__managers.remove(assigneeId)
        elif role == 2:
            self.__owners.remove(assigneeId)
        else:
            raise Exception("no such role")
        self.__appointers[assignerId].remove(assigneeId)

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
        self.__rating = (self.__numOfRating * self.__rating + rating) / (self.__numOfRating + 1)
        self.__numOfRating += 1
