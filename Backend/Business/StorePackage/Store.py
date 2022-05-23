import zope
from zope.interface import implements

from Backend.Exceptions.CustomExceptions import ProductException, PermissionException, TransactionException
from Backend.Interfaces.IMember import IMember
from Backend.Interfaces.IProduct import IProduct
from Backend.Interfaces.IStore import IStore
from Backend.Business.StorePackage.StorePermission import StorePermission
from Backend.Business.Transactions.StoreTransaction import StoreTransaction
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Business.DiscountPackage.DiscountComposite import DiscountComposite
from typing import Dict
import threading


@zope.interface.implementer(IStore)
class Store:

    def __init__(self, storeId, storeName, founder, bankAccount, address):
        self.__id = storeId
        self.__name = storeName
        self.__founderId = founder.getUserID()
        self.__bankAccount = bankAccount
        self.__address = address
        self.__appointers: Dict[IMember: []] = {}  # Member : Members list
        self.__managers = []  # Members
        self.__owners = [founder]  # Members
        self.__products: Dict[int: IProduct] = {}  # productId : Product
        self.__productsQuantity = {}  # productId : quantity
        self.__transactions: Dict[int: StoreTransaction] = {}
        self.__discounts: {int: IDiscount} = {}

        self.__permissionsLock = threading.Lock()
        self.__stockLock = threading.Lock()
        self.__productsLock = threading.Lock()
        self.__rolesLock = threading.Lock()
        self.__transactionLock = threading.Lock()
        self.__discountsLock = threading.Lock()

        self.__permissions: Dict[IMember: StorePermission] = {founder: StorePermission(founder.getUserID())}  # member : storePermission
        self.__permissions[founder].setPermission_AppointManager(True)
        self.__permissions[founder].setPermission_AppointOwner(True)
        self.__permissions[founder].setPermission_CloseStore(True)
        self.__permissions[founder].setPermission_StockManagement(True)
        self.__permissions[founder].setPermission_AppointManager(True)
        self.__permissions[founder].setPermission_AppointOwner(True)
        self.__permissions[founder].setPermission_ChangePermission(True)
        self.__permissions[founder].setPermission_CloseStore(True)
        self.__permissions[founder].setPermission_RolesInformation(True)
        self.__permissions[founder].setPermission_PurchaseHistoryInformation(True)
        self.__permissions[founder].setPermission_Discount(True)

    def getStoreId(self):
        return self.__id

    def getStoreName(self):
        return self.__name

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

    def getTransactionForDTO(self):
        return self.__transactions

    def getPermissionForDto(self):
        return self.__permissions

    def getProduct(self, productId):
        if productId in self.__products:
            return self.__products.get(productId)
        raise ProductException("product not in store")

    def getProductFromStore(self, productId):
        if productId in self.__products:
            return self.__products.get(productId)
        return None

    def hasProduct(self, productId):
        return productId in self.__products.keys()

    def setStockManagementPermission(self, assigner, assignee):
        try:
            if assignee not in self.__managers and assignee not in self.__owners:
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                self.__permissions[assignee].setPermission_StockManagement(True)

    def setAppointManagerPermission(self, assigner, assignee):
        try:
            if assignee not in self.__managers and assignee not in self.__owners:
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                self.__permissions[assignee].setPermission_AppointManager(True)

    def setAppointOwnerPermission(self, assigner, assignee):
        try:
            if assignee not in self.__owners:
                raise PermissionException("only owner can assign new owners")
            self.__haveAllPermissions(assigner, assignee)
            if assigner not in self.__owners:
                raise PermissionException("only owners can assign owners")
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                self.__permissions[assignee].setPermission_AppointOwner(True)

    def setChangePermission(self, assigner, assignee):
        try:
            if assignee not in self.__managers and assignee not in self.__owners:
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                self.__permissions[assignee].setPermission_ChangePermission(True)

    def setRolesInformationPermission(self, assigner, assignee):
        try:
            if assignee not in self.__managers and assignee not in self.__owners:
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                self.__permissions[assignee].setPermission_RolesInformation(True)

    def setPurchaseHistoryInformationPermission(self, assigner, assignee):
        try:
            if assignee not in self.__managers and assignee not in self.__owners:
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                self.__permissions[assignee].setPermission_PurchaseHistoryInformation(True)

    def setDiscountPermission(self, assigner, assignee):
        try:
            if assignee not in self.__managers and assignee not in self.__owners:
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                self.__permissions[assignee].setPermission_Discount(True)

    def __haveAllPermissions(self, assigner, assignee):
        # next version need to add parameter for removing.
        permissions = self.__permissions[assigner]
        if permissions is None:
            raise PermissionException("User ", assigner, " doesn't have any permissions is store: ", self.__id)
        if not permissions.hasPermission_ChangePermission():
            raise PermissionException("User ", assigner, "cannot change permission in store: ", self.__id)
        if assignee not in self.__appointers[assigner]:
            raise PermissionException("User ", assigner.getUserID(), "cannot change the permissions of user: ",
                                      assignee.getUserID(), " because he didn't assign him")

    def addProductToStore(self, user, product):
        try:
            self.__checkPermissions_ChangeStock(user)
            if product.getProductId() in self.__products.keys():
                raise ProductException("Product already exists!")
        except Exception as e:
            raise Exception(e)
        else:
            with self.__productsLock:
                self.__products[product.getProductId()] = product
            with self.__stockLock:
                self.__productsQuantity[product.getProductId()] = 0

    def addProductQuantityToStore(self, user, productId, quantity):
        try:
            self.__checkPermissions_ChangeStock(user)
            if self.__products.get(productId) is None:
                raise ProductException("cannot add quantity to a product who doesn't exist, in store: " + self.__name)
            if quantity <= 0:
                raise ProductException("cannot add a non-positive quantity")
        except Exception as e:
            raise Exception(e)
        else:
            with self.__stockLock:
                self.__productsQuantity[productId] += quantity

    def removeProductFromStore(self, user, productId):
        try:
            self.__checkPermissions_ChangeStock(user)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__productsLock:
                self.__products.pop(productId)
            with self.__stockLock:
                self.__productsQuantity.pop(productId)

    def updateProductPrice(self, user, productId, newPrice):
        try:
            self.__checkPermissions_ChangeStock(user)
            if self.__products.get(productId) is None:
                raise ProductException("cannot update to a product who doesn't exist, in store: " + self.__name)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__productsLock:
                self.__products.get(productId).setProductPrice(newPrice)
                return self.__products.get(productId)

    def updateProductName(self, user, productId, newName):
        try:
            self.__checkPermissions_ChangeStock(user)
            if self.__products.get(productId) is None:
                raise ProductException("cannot update to a product who doesn't exist, in store: " + self.__name)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__productsLock:
                self.__products.get(newName).setProductPrice(newName)
                return self.__products.get(productId)

    def updateProductCategory(self, user, productId, newCategory):
        try:
            self.__checkPermissions_ChangeStock(user)
            if self.__products.get(productId) is None:
                raise ProductException("cannot update to a product who doesn't exist, in store: " + self.__name)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__productsLock:
                self.__products.get(productId).setProductCategory(newCategory)
                return self.__products.get(productId)

    def updateProductWeight(self, user, productID, newWeight):
        try:
            self.__checkPermissions_ChangeStock(user)
            if self.__products.get(productID) is None:
                raise ProductException("cannot update to a product who doesn't exist, in store: " + self.__name)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__productsLock:
                self.__products.get(productID).setProductWeight(newWeight)
                return self.__products.get(productID)

    def __checkPermissions_ChangeStock(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store: ", self.__name)
        if not permissions.hasPermission_StockManagement():
            raise PermissionException("User ", user.getUserID(), " doesn't have the permission to change the stock in store: ",
                                      self.__name)

    def appointManagerToStore(self, assigner, assignee):
        permissions = self.__permissions.get(assigner)
        if assigner == assignee:
            raise PermissionException("User: ", assignee.getUserID(), " cannot assign himself to manager")
        if permissions is None:
            raise PermissionException("User ", assigner.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_AppointManager():
            raise PermissionException("User ", assigner.getUserID(), " doesn't have the permission - appoint manager in store: ",
                                      self.__name)
        if assigner not in self.__owners:
            raise PermissionException("User ", assigner.getUserID(), "cannot add manager to store: ", self.__name,
                                      "because he is not a store owner")
        # this constrains is also covert the constrains that for each manager there is 1 assigner
        if assignee in self.__managers:
            raise Exception("User ", assignee.getUserID(), "is all ready a manger in store: ", self.__name)
        # to avoid circularity
        if self.__appointers.get(assignee) is not None and assigner in self.__appointers.get(assigner):
            raise PermissionException("User ", assignee.getUserID(), "cannot assign manager to hwo made him owner in store: ",
                                      self.__name)

        with self.__rolesLock:
            self.__managers.append(assignee)
            if self.__appointers.get(assigner) is None:
                self.__appointers[assigner] = [assignee]
            else:
                self.__appointers[assigner].append(assignee)

        with self.__permissionsLock:
            if self.__permissions.get(assignee) is None:
                self.__permissions[assignee] = StorePermission(assignee.getUserID())
            self.__permissions[assignee].setPermission_PurchaseHistoryInformation(True)

    def appointOwnerToStore(self, assigner, assignee):
        permissions = self.__permissions.get(assigner)
        if assigner == assignee:
            raise PermissionException("User: ", assignee.getUserID(), " cannot assign himself to manager")
        if permissions is None:
            raise PermissionException("User ", assigner.getUserID(), " doesn't have any permissions is store:", str(self.__id))
        if not permissions.hasPermission_AppointOwner():
            raise PermissionException("User ", assigner.getUserID(), " doesn't have the permission - appoint owner in store: ",
                                      self.__name)
        if assigner not in self.__owners:
            raise PermissionException("User ", assigner.getUserID(), "cannot add manager to store: ", self.__name,
                                      "because he is not a store owner")
        # this constrains is also covert the constrains that for each owner there is 1 assigner
        if assignee in self.__owners:
            raise Exception("User ", assignee.getUserID(), "is all ready a owner in store: ", self.__name)
            # to avoid circularity
        if self.__appointers.get(assignee) is not None and assigner in self.__appointers.get(assigner):
            raise Exception("User ", assignee.getUserID(), "cannot assign owner to hwo made him manager in store: ", self.__name)

        with self.__rolesLock:
            self.__owners.append(assignee)

            if self.__appointers.get(assigner) is None:
                self.__appointers[assigner] = [assignee]
            else:
                self.__appointers[assigner].append(assignee)

        with self.__permissionsLock:
            if self.__permissions.get(assignee) is None:
                self.__permissions[assignee] = StorePermission(assignee.getUserID())
            self.__permissions[assignee].setPermission_StockManagement(True)
            self.__permissions[assignee].setPermission_AppointManager(True)
            self.__permissions[assignee].setPermission_AppointOwner(True)
            self.__permissions[assignee].setPermission_ChangePermission(True)
            self.__permissions[assignee].setPermission_RolesInformation(True)
            self.__permissions[assignee].setPermission_PurchaseHistoryInformation(True)
            self.__permissions[assignee].setPermission_Discount(True)

    def removeStoreOwner(self, assigner, assignee):
        if assigner not in self.__owners:
            raise Exception("user: " + str(assigner.getUserID()) + "is not an owner in store: " + str(self.__name))
        if assignee not in self.__owners:
            raise Exception("user: " + str(assignee) + "is not an owner in store: " + str(self.__name))
        if assignee not in self.__appointers.get(assigner):
            raise Exception("user: " + str(assigner.getUserID()) + "cannot remove the user: " +
                            str(assignee.getUserID() + "because he is not the one that appoint him"))
        self.__owners.remove(assignee)
        self.__appointers.get(assigner).remove(assignee)

    # print all permission in store - will be deleted this version
    def PrintRolesInformation(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_RolesInformation():
            raise PermissionException("User ", user.getUserID(),
                                      " doesn't have the permission - get roles information in store: ",
                                      self.__name)
        info = "info for store: " + self.__name + ":"
        info += "\n founderId: " + str(self.__founderId) + self.__permissions[self.__founderId].printPermission() + "\n"
        for owner in self.__owners:
            ownerId = owner.getUserID()
            if ownerId != self.__founderId:
                permission = self.__permissions[ownerId]
                info += "\n ownerId: " + str(ownerId) + permission.printPermission() + "\n"
        for managerId in self.__managers:
            permission = self.__permissions[managerId]
            info += "\n managerId: " + str(managerId) + permission.printPermission() + "\n"
        return info

    def getPermissions(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_RolesInformation():
            raise PermissionException("User ", user.getUserID(),
                                      " doesn't have the permission - get roles information in store: ",
                                      self.__name)
        return self.__permissions.values()

    def addTransaction(self, transaction):
        with self.__transactionLock:
            self.__transactions[transaction.getTransactionID()] = transaction

    def removeTransaction(self, transactionId):
        with self.__transactions:
            if transactionId in self.__transactions.keys():
                self.__transactions.pop(transactionId)

    def getTransaction(self, transactionId):
        if transactionId not in self.__transactions.keys():
            raise TransactionException("in store: ", self.__id, "there is not transaction with Id: ", transactionId)
        self.__transactions.get(transactionId)

    # print all transactions in store - will be deleted in this version
    def printPurchaseHistoryInformation(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_RolesInformation():
            raise PermissionException("User ", user.getUserID(),
                                      " doesn't have the permission - get roles information in store: ",
                                      self.__name)
        info = "purchase history for store: " + self.__storeName + " ,storeId: " + str(self.__storeId) + " :\n"
        for storeTransaction in self.__transactions:
            info += storeTransaction.getPurchaseHistoryInformation() + "\n"
        return info

    def getTransactionHistory(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_RolesInformation():
            raise PermissionException("User ", user.getUserID(),
                                      " doesn't have the permission - get roles information in store: ",
                                      self.__name)
        return self.__transactions.values()

    def getProductsByName(self, productName):
        toReturnProducts = []
        for product in self.__products.values():
            if product.getProductName().lower() == productName.lower():
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
            if product.getProductCategory().lower() == productCategory.lower():
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
        if self.__products.get(productId) is None:
            raise ProductException("product: ", productId, "cannot be added because he is not in store: ", self.__id)
        if self.__productsQuantity[productId] < quantity:
            raise ProductException("cannot add a negative quantity to bag")
        else:
            with self.__stockLock:
                self.__productsQuantity[productId] -= quantity
                return True

    def removeProductFromBag(self, productId, quantity):
        if productId not in self.__products.keys():
            raise ProductException("product: ", productId, "cannot be remove because he is not in store: ", self.__id)
        with self.__stockLock:
            self.__productsQuantity[productId] += quantity

    def hasRole(self, user):
        return user in self.__owners or user in self.__managers

    def getTransactionsForSystemManager(self):
        return self.__transactions.values()

    def hasPermissions(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            return False
        return True

    def addSimpleDiscount(self, user, discount):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID()," doesn't have the discount permission in store: ",self.__name)
        with self.__discountsLock:
            self.__discounts[discount.getDiscountId()] = discount

    def addCompositeDiscount(self, user, discountId, dId1, dId2, discountType):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        d1 = self.__discounts.get(dId1)
        d2 = self.__discounts.get(dId2)
        if d1 is None:
            raise Exception("discount1 is not an existing discount")
        if d2 is None:
            raise Exception("discount1 is not an existing discount")
        discount = DiscountComposite(discountId, d1, d2, discountType)
        with self.__discountsLock:
            self.__discounts[discount.getDiscountId()] = discount
            self.__discounts.pop(dId1)
            self.__discounts.pop(dId2)
        return discount

    def removeDiscount(self, user, discount):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        if discount not in self.__discounts:
            raise Exception("the discount is not an existing discount")
        with self.__discountsLock:
            self.__discounts.pop(discount.getDiscountId())
        return True

    def getAllDiscounts(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        return self.__discounts

    def hasDiscountPermission(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        return permissions.hasPermission_Discount()
