from interface import implements
from interfaces import IStore


class Store(implements(IStore)):

    def __init__(self, storeId, storeName, founderId):
        self.__id = storeId
        self.__name = storeName
        self.__founderId = founderId
        self.__permissions = {}  # <UserId,permission>
        self.__appointers = {}  # <UserId,UserId>
        self.__products = {}  # productId : Product
        self.__transactions = {}  # transactionId : Transaction
        self.__discountPolicy = None
        self.__discounts = {}  # discountType/Id : Discount

    def getStoreId(self):
        return self.__id

    def getStoreFounderId(self):
        return self.__founderId

    def getStoreOwners(self):
        pass

    def getStoreManagers(self):
        pass

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

    def __checkPermissions(self, userId, line):
        permissions = self.__permissions[userId]
        if permissions is None:
            raise Exception("User ", userId, " doesn't have any permissions is store:", self.__id)
        if not permissions.hasPremission_AddProduct():
            raise Exception("User ", userId, " doesn't have the permission - ", line, " in  store:", self.__id)

    def addRole(self, assignerId, assigneeId, ruleId):
        pass

    def addDiscount(self, userId, Discount):
        pass

    def removeDiscount(self, userId, Discount):
        pass

    def updateDiscount(self, userId, discountId, newDiscount):
        pass

    def addTransaction(self, transaction):
        pass

    def removeTransaction(self, transaction):
        pass

    def getStoreTransactionHistory(self):
        pass

    def editPermission(self, assignerId, assigneeId):
        pass
