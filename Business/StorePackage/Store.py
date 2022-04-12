from interface import implements
from interfaces import IStore


class Store(implements(IStore)):

    def __init__(self, storeId, storeName, founderId):
        self.id = storeId
        self.name = storeName
        self.founderId = founderId
        self.owners = dict()    # ownerId : User
        self.managers = dict()  # managerId : User
        self.products = dict()  # productId : Product
        self.transactions = dict()  # transactionId : Transaction
        self.discountPolicy = None
        self.discounts = dict()  # discountType/Id : Discount

    def getStoreId(self):
        pass

    def getStoreFounder(self):
        pass

    def getStoreOwners(self):
        pass

    def getStoreManagers(self):
        pass

    def addProduct(self, userId, product):
        pass

    def removeProduct(self, userId, product):
        pass

    def updateProduct(self, userId, productId, newProduct):
        pass

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
