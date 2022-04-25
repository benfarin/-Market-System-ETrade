from interface import implements
from interfaces.IStore import IStore
from Business.StorePackage.StorePermission import StorePermission
from Business.Transactions.StoreTransaction import StoreTransaction
from typing import Dict, List
import uuid


class Store(implements(IStore)):

    def __init__(self, storeId, storeName, founderId, bankAccount, address):
        self.__id = storeId
        self.__name = storeName
        self.__founderId = founderId
        self.__bankAccount = bankAccount
        self.__address = address
        self.__appointers: Dict[str: List] = {}  # UserId : UserId list
        self.__managers = []  # userId
        self.__owners = [self.__founderId]  # userId
        self.__products = {}  # productId : Product
        self.__productsQuantity = {}  # productId : quantity
        self.__transactions = StoreTransaction(storeId, storeName)

        self.__permissions: Dict[str: StorePermission] = {founderId: StorePermission()}  # UserId : storePermission
        self.__permissions[founderId].setPermission_AppointManager(True)
        self.__permissions[founderId].setPermission_AppointOwner(True)
        self.__permissions[founderId].setPermission_CloseStore(True)
        self.__permissions[founderId].setPermission_StockManagement(True)
        self.__permissions[founderId].setPermission_AppointManager(True)
        self.__permissions[founderId].setPermission_AppointOwner(True)
        self.__permissions[founderId].setPermission_ChangePermission(True)
        self.__permissions[founderId].setPermission_RolesInformation(True)
        self.__permissions[founderId].setPermission_PurchaseHistoryInformation(True)

    def getStoreId(self):
        return self.__id

    def getStoreFounderId(self):
        return self.__founderId

    def getStoreBankAccount(self):
        return self.__bankAccount

    def getStoreAddress(self):
        return self.__address

    def getStoreOwners(self):
        return self.__owners

    def getStoreManagers(self):
        return self.__managers

    def getProducts(self):
        return self.__products

    def getProductQuantity(self):
        return self.__productsQuantity

    def getProduct(self, productId):
        if productId in self.__products:
            return self.__products[productId]
        raise Exception("product not in store")

    def hasProduct(self, productId):
        return productId in self.__products.keys()

    def setStockManagementPermission(self, assignerId, assigneeId):
        try:
            if assigneeId not in self.__managers and assigneeId not in self.__owners:
                raise Exception("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_StockManagement(True)
        except Exception as e:
            raise Exception(e)

    def setAppointManagerPermission(self, assignerId, assigneeId):
        try:
            if assigneeId not in self.__managers and assigneeId not in self.__owners:
                raise Exception("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_AppointManager(True)
        except Exception as e:
            raise Exception(e)

    def setAppointOwnerPermission(self, assignerId, assigneeId):
        try:
            if assigneeId not in self.__owners:
                raise Exception("only owner can assign new owners")
            self.__haveAllPermissions(assignerId, assigneeId)
            if assignerId not in self.__owners:
                raise Exception("only owners can assign owners")
            self.__permissions[assigneeId].setPermission_AppointOwner(True)
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, assignerId, assigneeId):
        try:
            if assigneeId not in self.__managers and assigneeId not in self.__owners:
                raise Exception("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_ChangePermission(True)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, assignerId, assigneeId):
        try:
            if assigneeId not in self.__managers and assigneeId not in self.__owners:
                raise Exception("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_RolesInformation(True)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, assignerId, assigneeId):
        try:
            if assigneeId not in self.__managers and assigneeId not in self.__owners:
                raise Exception("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assignerId, assigneeId)
            self.__permissions[assigneeId].setPermission_PurchaseHistoryInformation(True)
        except Exception as e:
            raise Exception(e)

    def __haveAllPermissions(self, assignerId, assigneeId):
        # next version need to add parameter for removing.
        permissions = self.__permissions[assignerId]
        if permissions is None:
            raise Exception("User ", assignerId, " doesn't have any permissions is store: ", self.__id)
        if not permissions.hasPermission_ChangePermission():
            raise Exception("User ", assignerId, "cannot change permission in store: ", self.__id)
        if assigneeId not in self.__appointers[assignerId]:
            raise Exception("User ", assignerId, "cannot change the permissions of user: ", assigneeId,
                            " because he didn't assign him")

    def addProductToStore(self, userId, product):
        try:
            self.__checkPermissions_ChangeStock(userId)
            if product.getProductId in self.__products.keys():
                raise Exception("product all ready in store")
            self.__products[product.getProductId()] = product
            self.__productsQuantity[product.getProductId()] = 0
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, userId, productId, quantity):
        try:
            self.__checkPermissions_ChangeStock(userId)
            if self.__products[productId] is None:
                raise Exception("cannot add quantity to a product who doesn't exist, in store: " + self.__name)
            self.__productsQuantity[productId] += quantity
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, userId, productId):
        try:
            self.__checkPermissions_ChangeStock(userId)
            self.__products.pop(productId)
        except Exception as e:
            raise Exception(e)

    def updateProductFromStore(self, userId, productId, newProduct):
        try:
            self.__checkPermissions_ChangeStock(userId)
            if self.__products[productId] is None:
                raise Exception("cannot update to a product who doesn't exist, in store: " + self.__name)
            self.__products[productId] = newProduct
        except Exception as e:
            raise Exception(e)

    def __checkPermissions_ChangeStock(self, userId):
        permissions = self.__permissions[userId]
        if permissions is None:
            raise Exception("User ", userId, " doesn't have any permissions is store: ", self.__name)
        if not permissions.hasPermission_StockManagement():
            raise Exception("User ", userId, " doesn't have the permission to change the stock in store: ", self.__name)

    def appointManagerToStore(self, assignerId, assigneeId):
        permissions = self.__permissions[assignerId]
        if assignerId == assigneeId:
            raise Exception("User: ", assigneeId, " cannot assign himself to manager")
        if permissions is None:
            raise Exception("User ", assignerId, " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_AppointManager():
            raise Exception("User ", assignerId, " doesn't have the permission - appoint manager in store: ",
                            self.__name)
        if assignerId not in self.__owners:
            raise Exception("User ", assignerId, "cannot add manager to store: ", self.__name,
                            "because he is not a store owner")
        # this constrains is also covert the constrains that for each manager there is 1 assigner
        if assigneeId in self.__managers:
            raise Exception("User ", assigneeId, "is all ready a manger in store: ", self.__name)
        # to avoid circularity
        if self.__appointers.get(assigneeId) is not None and assignerId in self.__appointers.get(assigneeId):
            raise Exception("User ", assigneeId, "cannot assign manager to hwo made him owner in store: ", self.__name)

        self.__managers.append(assigneeId)
        if self.__appointers.get(assignerId) is None:
            self.__appointers[assignerId] = [assigneeId]
        else:
            self.__appointers[assignerId].append(assigneeId)

        if self.__permissions.get(assigneeId) is None:
            self.__permissions[assigneeId] = StorePermission()
        self.__permissions[assigneeId].setPermission_PurchaseHistoryInformation(True)

    def appointOwnerToStore(self, assignerId, assigneeId):
        permissions = self.__permissions[assignerId]
        if assignerId == assigneeId:
            raise Exception("User: ", assigneeId, " cannot assign himself to manager")
        if permissions is None:
            raise Exception("User ", assignerId, " doesn't have any permissions is store:", self.__id)
        if not permissions.hasPermission_AppointOwner():
            raise Exception("User ", assignerId, " doesn't have the permission - appoint owner in store: ",
                            self.__name)
        if assignerId not in self.__owners:
            raise Exception("User ", assignerId, "cannot add manager to store: ", self.__name,
                            "because he is not a store owner")
        # this constrains is also covert the constrains that for each owner there is 1 assigner
        if assigneeId in self.__owners:
            raise Exception("User ", assigneeId, "is all ready a owner in store: ", self.__name)
            # to avoid circularity
        if self.__appointers.get(assigneeId) is not None and assignerId in self.__appointers.get(assigneeId):
            raise Exception("User ", assigneeId, "cannot assign owner to hwo made him manager in store: ", self.__name)

        self.__owners.append(assigneeId)

        if self.__appointers.get(assignerId) is None:
            self.__appointers[assignerId] = [assigneeId]
        else:
            self.__appointers[assignerId].append(assigneeId)

        if self.__permissions.get(assigneeId) is None:
            self.__permissions[assigneeId] = StorePermission()
        self.__permissions[assigneeId].setPermission_StockManagement(True)
        self.__permissions[assigneeId].setPermission_AppointManager(True)
        self.__permissions[assigneeId].setPermission_AppointOwner(True)
        self.__permissions[assigneeId].setPermission_ChangePermission(True)
        self.__permissions[assigneeId].setPermission_RolesInformation(True)
        self.__permissions[assigneeId].setPermission_PurchaseHistoryInformation(True)

    # print all permission in store
    def PrintRolesInformation(self, userId):
        permissions = self.__permissions[userId]
        if permissions is None:
            raise Exception("User ", userId, " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_RolesInformation():
            raise Exception("User ", userId, " doesn't have the permission - get roles information in store: ",
                            self.__name)
        info = "info for store: " + self.__name + ":"
        info += "\n founderId: " + str(self.__founderId) + self.__permissions[self.__founderId].printPermission() + "\n"
        for ownerId in self.__owners:
            if ownerId != self.__founderId:
                permission = self.__permissions[ownerId]
                info += "\n ownerId: " + str(ownerId) + permission.printPermission() + "\n"
        for managerId in self.__managers:
            permission = self.__permissions[managerId]
            info += "\n managerId: " + str(managerId) + permission.printPermission() + "\n"
        return info

    def getPermissions(self, userId):
        permissions = self.__permissions[userId]
        if permissions is None:
            raise Exception("User ", userId, " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_RolesInformation():
            raise Exception("User ", userId, " doesn't have the permission - get roles information in store: ",
                            self.__name)
        return self.__permissions

    def addTransaction(self, transaction):
        self.__transactions.addTransaction(transaction)

    def removeTransaction(self, transactionId):
        try:
            self.__transactions.removeTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    # print all transactions in store
    def printPurchaseHistoryInformation(self, userId):
        permissions = self.__permissions[userId]
        if permissions is None:
            raise Exception("User ", userId, " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_RolesInformation():
            raise Exception("User ", userId, " doesn't have the permission - get roles information in store: ",
                            self.__name)
        return self.__storeHistory.getPurchaseHistoryInformation()

    def getTransactionHistory(self, userId):
        permissions = self.__permissions[userId]
        if permissions is None:
            raise Exception("User ", userId, " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_RolesInformation():
            raise Exception("User ", userId, " doesn't have the permission - get roles information in store: ",
                            self.__name)
        return self.__storeHistory.getTransactionHistory()

    def getProductsByName(self, productName):
        toReturnProducts = []
        for product in self.__products.values():
            if product.getProductName() == productName:
                toReturnProducts.append(product)
        return toReturnProducts

    def getProductsByKeyword(self, keyword):
        products = []
        for product in self.__products.values():
            if product.isExistsKeyword(keyword):
                products.append(product)
        return products

    def getProductsByCategory(self, productCategory):
        toReturnProducts = []
        for product in self.__products.values():
            if product.getProductCategory() == productCategory:
                toReturnProducts.append(product)
        return toReturnProducts

    def getProductsByPriceRange(self, minPrice, maxPrice):
        toReturnProducts = []
        for product in self.__products.values():
            price = product.getProductPrice()
            if minPrice <= price <= maxPrice:
                toReturnProducts.append(product)
        return toReturnProducts

    def addProductToBag(self, productId, quantity):
        if productId not in self.__products.keys():
            raise Exception("product: ", productId, "cannot be added because he is not in store: ", self.__id)
        if self.__productsQuantity[productId] < quantity:
            return False
        else:
            self.__productsQuantity[productId] -= quantity
            return True

    def removeProductFromBag(self, productId, quantity):
        if productId not in self.__products.keys():
            raise Exception("product: ", productId, "cannot be remove because he is not in store: ", self.__id)
        self.__productsQuantity[productId] += quantity
