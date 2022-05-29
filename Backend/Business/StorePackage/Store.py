import zope
from zope.interface import implements
import os, django

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount
from Backend.Business.Rules import QuantityRule, WeightRule
from Backend.Business.Rules.DiscountRuleComposite import DiscountRuleComposite
from Backend.Business.Rules.PriceRule import PriceRule
from Backend.Business.StorePackage.Product import Product
import Backend.Business.UserPackage.Member as m

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from Backend.Business.Address import Address
from Backend.Business.Bank import Bank
from Backend.Business.Rules.PurchaseRuleComposite import PurchaseRuleComposite
from Backend.Exceptions.CustomExceptions import ProductException, PermissionException, TransactionException
from Backend.Interfaces.IMember import IMember
from Backend.Interfaces.IProduct import IProduct
from Backend.Interfaces.IRule import IRule
from Backend.Interfaces.IStore import IStore
from Backend.Business.StorePackage.StorePermission import StorePermission
from Backend.Business.Transactions.StoreTransaction import StoreTransaction
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from typing import Dict
import threading
from notifications.signals import notify

from ModelsBackend.models import StoreModel, StoreUserPermissionsModel, ProductModel, \
    ProductsInStoreModel, StoreAppointersModel, TransactionsInStoreModel, StoreTransactionModel, DiscountsInStoreModel, \
    DiscountModel, RulesInStoreModel, RuleModel


@zope.interface.implementer(IStore)
class Store:

    def __init__(self, storeId, storeName, founder, bankAccount, address):
        # self.__id = storeId
        # self.__name = storeName
        # self.__founderId = founder.getUserID()
        # self.__bankAccount: Bank = bankAccount
        # self.__address: Address = address
        # self.__appointers: Dict[IMember: []] = {}  # Member : Members list
        # self.__managers = []  # Members
        # self.__owners = [founder]  # Members
        # self.__products: Dict[int: IProduct] = {}  # productId : Product
        # self.__productsQuantity = {}  # productId : quantity
        # self.__transactions: Dict[int: StoreTransaction] = {}
        # self.__discounts: {int: IDiscount} = {}
        # self.__rules: {int: IRule} = {}

        self.__model = StoreModel.objects.get_or_create(storeID=storeId, name=storeName, founderId=founder.getModel(),
                              bankAccount=bankAccount.getModel(), address=address.getModel())[0]
        self.__model.owners.add(founder.getModel())

        # self.__permissionsLock = threading.Lock()
        # self.__stockLock = threading.Lock()
        # self.__productsLock = threading.Lock()
        # self.__rolesLock = threading.Lock()
        # self.__transactionLock = threading.Lock()
        # self.__discountsLock = threading.Lock()

        # self.__permissions: Dict[IMember: StorePermission] = {
        #     founder: StorePermission(founder.getUserID())}  # member : storePermission
        # self.__permissions[founder].setPermission_AppointManager(True)
        # self.__permissions[founder].setPermission_AppointOwner(True)
        # self.__permissions[founder].setPermission_CloseStore(True)
        # self.__permissions[founder].setPermission_StockManagement(True)
        # self.__permissions[founder].setPermission_AppointManager(True)
        # self.__permissions[founder].setPermission_AppointOwner(True)
        # self.__permissions[founder].setPermission_ChangePermission(True)
        # self.__permissions[founder].setPermission_CloseStore(True)
        # self.__permissions[founder].setPermission_RolesInformation(True)
        # self.__permissions[founder].setPermission_PurchaseHistoryInformation(True)
        # self.__permissions[founder].setPermission_Discount(True)

        self.__permissions_model= StoreUserPermissionsModel.objects.get_or_create(userID=founder.getModel(), storeID=self.__model, appointManager=True,
                                                 appointOwner=True, closeStore=True, stockManagement=True,
                                                 changePermission=True, rolesInformation=True,
                                                 purchaseHistoryInformation=True, discount=True)[0]

    def getStoreId(self):
        return self.__model.storeID

    def getStoreName(self):
        return self.__model.name

    def getStoreFounderId(self):
        return self.__model.founderId

    def getStoreBankAccount(self):
        return self._buildBankAccount(self.__model.bankAccount)

    def getStoreAddress(self):
        return self._buildAddress(self.__model.address)

    def getStoreOwners(self):
        owners = []
        store_model = StoreModel.objects.get(storeID=self.getStoreId())
        for owner_model in store_model.owners.get_queryset():
            owner = self._buildMember(owner_model)
            owners.append(owner)
        return owners

    def getStoreManagers(self):
        managers = []
        store_model = StoreModel.objects.get(storeID=self.getStoreId())
        for manager_model in store_model.managers.get_queryset():
            manager = self._buildMember(manager_model)
            managers.append(manager)
        return managers

    def getProducts(self):
        products: Dict[int: IProduct] = {}
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model):
            product = self._buildProduct(prod.productID)
            products.update({product.getProductId() : product})
        return products

    def getProductQuantity(self):
        productsQuantity = {}
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model):
            productsQuantity[prod.productID.product_id] = prod.quantity
        return productsQuantity

    def getTransactionForDTO(self):  ###NEED TO CHANGE THIS
        return self.__transactions

    def getPermissionForDto(self): ###NEED TO CHANGE THIS
        return self.__permissions

    def getProduct(self, productId):
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model):
            if prod.productID.product_id == productId:
                return self._buildProduct(prod.productID)
        raise ProductException("product not in store")


    def setStockManagementPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).stockManagement = True
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).save()
            # with self.__permissionsLock:
            #     self.__permissions[assignee].setPermission_StockManagement(True)

    def setAppointManagerPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).appointManager = True
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).save()
            # with self.__permissionsLock:
            #     self.__permissions[assignee].setPermission_AppointManager(True)

    def setAppointOwnerPermission(self, assigner, assignee):
        try:
            if assignee not in  self.getStoreOwners():
                raise PermissionException("only owner can assign new owners")
            self.__haveAllPermissions(assigner, assignee)
            if assigner not in self.getStoreOwners():
                raise PermissionException("only owners can assign owners")
        except Exception as e:
            raise Exception(e)
        else:
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).appointOwner = True
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).save()
            # with self.__permissionsLock:
            #     self.__permissions[assignee].setPermission_AppointOwner(True)

    def setChangePermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).changePermission = True
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).save()

    def setRolesInformationPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).rolesInformation = True
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).save()

    def setPurchaseHistoryInformationPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).purchaseHistoryInformation = True
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).save()

    def setDiscountPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).discount = True
            StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model).save()

    def __haveAllPermissions(self, assigner, assignee):
        # next version need to add parameter for removing.
        permissions = StoreUserPermissionsModel.objects.filter(userID=assigner.getModel(), storeID=self.__model)
        if not permissions.exists():
            raise PermissionException("User ", assigner, " doesn't have any permissions is store: ", self.__id)
        if not permissions.first().changePermission:
            raise PermissionException("User ", assigner, "cannot change permission in store: ", self.__id)
        if not StoreUserPermissionsModel.objects.filter(userID=assignee.getModel(), storeID=self.__model).exists():
            raise PermissionException("User ", assigner.getUserID(), "cannot change the permissions of user: ",
                                      assignee.getUserID(), " because he didn't assign him")

    def addProductToStore(self, user, product):
        try:
            self.__checkPermissions_ChangeStock(user)
            if ProductsInStoreModel.objects.filter(storeID=self.__model, productID=product.getModel()).exists():
                raise ProductException("Product already exists!")
        except Exception as e:
            raise Exception(e)
        else:
            ProductsInStoreModel.objects.get_or_create(storeID=self.__model, productID=product.getModel(), quantity=0)

    def addProductQuantityToStore(self, user, productId, quantity):
        try:
            self.__checkPermissions_ChangeStock(user)
            product_model = ProductModel.objects.get_or_create(product_id=productId)
            if not ProductsInStoreModel.objects.filter(storeID=self.__model, productID=product_model).exists():
                raise ProductException("cannot add quantity to a product who doesn't exist, in store: " + self.__name)
            if quantity <= 0:
                raise ProductException("cannot add a non-positive quantity")
        except Exception as e:
            raise Exception(e)
        else:
            with self.__stockLock:
                self.__productsQuantity[productId] += quantity
                quantity = ProductsInStoreModel(storeID=self.__model,
                                                     productID=ProductModel.objects.get(product_id=productId),
                                                     quantity=quantity)
                quantity.save()

    def removeProductFromStore(self, user, productId):
        try:
            self.__checkPermissions_ChangeStock(user)
        except Exception as e:
            raise Exception(e)
        else:
            product_model = ProductModel.objects.get_or_create(product_id=productId)[0]
            ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model).delete()


    def updateProductPrice(self, user, productId, newPrice):
        try:
            self.__checkPermissions_ChangeStock(user)
            product_model = ProductModel.objects.get_or_create(product_id=productId)[0]
            if not ProductsInStoreModel.objects.filter(storeID=self.__model, productID=product_model).exists():
                raise ProductException("cannot update to a product who doesn't exist, in store: " + self.__name)
        except Exception as e:
            raise Exception(e)
        else:
            product = self._buildProduct(product_model)
            product.setProductPrice(newPrice)
            return product

    def updateProductName(self, user, productId, newName):
        try:
            self.__checkPermissions_ChangeStock(user)
            product_model = ProductModel.objects.get_or_create(product_id=productId)[0]
            if not ProductsInStoreModel.objects.filter(storeID=self.__model, productID=product_model).exists():
                raise ProductException("cannot update to a product who doesn't exist, in store: " + self.__name)
        except Exception as e:
            raise Exception(e)
        else:
            product = self._buildProduct(product_model)
            product.setProductName(newName)
            return product

    def updateProductCategory(self, user, productId, newCategory):
        try:
            self.__checkPermissions_ChangeStock(user)
            product_model = ProductModel.objects.get_or_create(product_id=productId)[0]
            if not ProductsInStoreModel.objects.filter(storeID=self.__model, productID=product_model).exists():
                raise ProductException("cannot update to a product who doesn't exist, in store: " + self.__name)
        except Exception as e:
            raise Exception(e)
        else:
            product = self._buildProduct(product_model)
            product.setProductCategory(newCategory)
            return product

    def updateProductWeight(self, user, productID, newWeight):
        try:
            self.__checkPermissions_ChangeStock(user)
            product_model = ProductModel.objects.get_or_create(product_id=productID)[0]
            if not ProductsInStoreModel.objects.filter(storeID=self.__model, productID=product_model).exists():
                raise ProductException("cannot update to a product who doesn't exist, in store: " + self.__name)
        except Exception as e:
            raise Exception(e)
        else:
            product = self._buildProduct(product_model)
            product.setProductWeight(newWeight)
            return product

    def __checkPermissions_ChangeStock(self, user):
        permissions = StoreUserPermissionsModel.objects.filter(userID=user.getModel(), storeID=self.__model)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store: ",
                                      self.__name)
        if not permissions.first().stockManagement:
            raise PermissionException("User ", user.getUserID(),
                                      " doesn't have the permission to change the stock in store: ",
                                      self.__name)

    def appointManagerToStore(self, assigner, assignee):  ####NEED TO CHANGE THIS
        permissions = self.__permissions.get(assigner)
        if assigner == assignee:
            raise PermissionException("User: ", assignee.getUserID(), " cannot assign himself to manager")
        if permissions is None:
            raise PermissionException("User ", assigner.getUserID(), " doesn't have any permissions is store:",
                                      self.__name)
        if not permissions.hasPermission_AppointManager():
            raise PermissionException("User ", assigner.getUserID(),
                                      " doesn't have the permission - appoint manager in store: ",
                                      self.__name)
        if assigner not in self.__owners:
            raise PermissionException("User ", assigner.getUserID(), "cannot add manager to store: ", self.__name,
                                      "because he is not a store owner")
        # this constrains is also covert the constrains that for each manager there is 1 assigner
        if assignee in self.__managers:
            raise Exception("User ", assignee.getUserID(), "is all ready a manger in store: ", self.__name)
        # to avoid circularity
        if self.__appointers.get(assignee) is not None and assigner in self.__appointers.get(assigner):
            raise PermissionException("User ", assignee.getUserID(),
                                      "cannot assign manager to hwo made him owner in store: ",
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
                StoreUserPermissionsModel(userID=assignee.getModel(), storeID=self.__s).save()
            self.__permissions[assignee].setPermission_PurchaseHistoryInformation(True)
            permission = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__s)
            permission.rolesInformation = True
            permission.save()

    def appointOwnerToStore(self, assigner, assignee):    ####NEED TO CHANGE THIS
        permissions = self.__permissions.get(assigner)
        if assigner == assignee:
            raise PermissionException("User: ", assignee.getUserID(), " cannot assign himself to manager")
        if permissions is None:
            raise PermissionException("User ", assigner.getUserID(), " doesn't have any permissions is store:",
                                      str(self.__id))
        if not permissions.hasPermission_AppointOwner():
            raise PermissionException("User ", assigner.getUserID(),
                                      " doesn't have the permission - appoint owner in store: ",
                                      self.__name)
        if assigner not in self.__owners:
            raise PermissionException("User ", assigner.getUserID(), "cannot add manager to store: ", self.__name,
                                      "because he is not a store owner")
        # this constrains is also covert the constrains that for each owner there is 1 assigner
        if assignee in self.__owners:
            raise Exception("User ", assignee.getUserID(), "is all ready a owner in store: ", self.__name)
            # to avoid circularity
        if self.__appointers.get(assignee) is not None and assigner in self.__appointers.get(assigner):
            raise Exception("User ", assignee.getUserID(), "cannot assign owner to hwo made him manager in store: ",
                            self.__name)

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

    # if the owner was also a manager, need to give the assignee all his permission from the start.
    def removeStoreOwner(self, assigner, assignee):
        if assigner not in self.getStoreOwners():
            raise Exception("user: " + str(assigner.getUserID()) + "is not an owner in store: " + str(self.__name))
        if assignee not in self.getStoreOwners():
            raise Exception("user: " + str(assignee) + "is not an owner in store: " + str(self.__name))
        if not StoreAppointersModel.objects.filter(storeID=self.__model, assigner=assigner.getModel(), assingee=assignee.getModel()).exists():
            raise Exception("user: " + str(assigner.getUserID()) + "cannot remove the user: " +
                            str(assignee.getUserID() + "because he is not the one that appoint him"))

        assignees_of_assignee = StoreAppointersModel.objects.filter(storeID=self.__model, assigner=assigner.getModel())
        if assignees_of_assignee.exists():
            for toRemoveOwner in assignees_of_assignee:
                to_remove = self._buildMember(toRemoveOwner.assingee)
                self.removeStoreOwner(assignee, to_remove)
        StoreUserPermissionsModel.objects.get(storeID=self.__model, userID=assignee.getModel()).delete()
        for model in StoreModel.objects.get(storeID=self.__model).owners.get_queryset():
            if assignee.getModel() == model:
                model.delete()
        StoreAppointersModel.objects.get(storeID=self.__model, assigner=assigner.getModel(), assingee=assignee.getModel()).delete()

    # print all permission in store - will be deleted this version
    def PrintRolesInformation(self, user):   ####NEED TO CHANGE THIS
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

    def getPermissions(self, user):  ### NEED TO CHANGE + NO USE OF THIS FUNCTIONS?
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.first().rolesInformation:
            raise PermissionException("User ", user.getUserID(),
                                      " doesn't have the permission - get roles information in store: ",
                                      self.__name)
        return self.__permissions.values()

    def addTransaction(self, transaction):
        TransactionsInStoreModel.objects.get_or_create(storeID=self.__model, transactionID=transaction.getModel())

    def removeTransaction(self, transactionId):
        transaction_model = StoreTransactionModel.objects.get(transactionId=transactionId)
        TransactionsInStoreModel.objects.get(storeID=self.__model, transactionID=transaction_model).delete()


    def getTransaction(self, transactionId):
        if not StoreTransactionModel.objects.filter(transactionId=transactionId).exists():
            raise TransactionException("in store: ", self.__id, "there is not transaction with Id: ", transactionId)
        transaction_model = StoreTransactionModel.objects.get(transactionId=transactionId)
        return self._buildStoreTransactions(transaction_model)

    # print all transactions in store - will be deleted in this version
    def printPurchaseHistoryInformation(self, user):  ###NEED TO CHANGE THIS
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

    def getTransactionHistory(self, user):  ###NEED TO CHANGE THIS
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
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model):
            product = self._buildProduct(prod.productID)
            if product.getProductName().lower() == productName.lower():
                toReturnProducts.append(product)
        return toReturnProducts

    def getProductsByKeyword(self, keyword):
        products = []
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model):
            product = self._buildProduct(prod.productID)
            if product.isExistsKeyword(keyword):
                products.append(product)
        return products

    def getProductsByCategory(self, productCategory):
        toReturnProducts = []
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model):
            product = self._buildProduct(prod.productID)
            if product.getProductCategory().lower() == productCategory.lower():
                toReturnProducts.append(product)
        return toReturnProducts

    def getProductsByPriceRange(self, minPrice, maxPrice):
        toReturnProducts = []
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model):
            product = self._buildProduct(prod.productID)
            price = product.getProductPrice()
            if minPrice <= price <= maxPrice:
                toReturnProducts.append(product)
        return toReturnProducts

    def addProductToBag(self, productId, quantity):   ###NO USE OF THIS FUNCTION - NEED TO DELETE IT?
        product_model = ProductModel.objects.get(product_id=productId)
        if not ProductsInStoreModel.objects.filter(storeID=self.__model, productID=product_model).exists():
            raise ProductException("product: ", productId, "cannot be added because he is not in store: ", self.__id)
        if ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model).quantity < quantity:
            raise ProductException("cannot add a negative quantity to bag")
        else:
            ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model).quantity -= quantity
            ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model).save()

    def removeProductFromBag(self, productId, quantity):    ###NO USE OF THIS FUNCTION - NEED TO DELETE IT?
        if not ProductModel.objects.filter(product_id=productId).exists():
            raise ProductException("product: ", productId, "cannot be remove because he is not in store: ", self.__id)
        product_model = ProductModel.objects.get(product_id=productId)
        ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model).quantity += quantity
        ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model).save()

    def hasRole(self, user):
        return user in self.getStoreOwners() or user in self.getStoreManagers()

    def getTransactionsForSystemManager(self):   ###NEED TO CHANGE THIS
        return self.__transactions.values()

    def hasPermissions(self, user):
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            return False
        return True

    def addSimpleDiscount(self, user, discount):
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.first().discount:
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        DiscountsInStoreModel.objects.get_or_create(storeID=self.__model, discountID=discount.getModel())

    def addCompositeDiscount(self, user, discountId, dId1, dId2, discountType, decide):   ###NEED TO CHANGE THIS
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
        discount = DiscountComposite(discountId, d1, d2, discountType, decide)
        with self.__discountsLock:
            self.__discounts[discount.getDiscountId()] = discount
            self.__discounts.pop(dId1)
            self.__discounts.pop(dId2)
        return discount

    def removeDiscount(self, user, dId):
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.first().discount:
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        discount_model = DiscountModel.objects.get(discountID=dId)
        discount = DiscountsInStoreModel.objects.filter(storeID=self.__model, discountID=discount_model)
        if not discount.exists():
            raise Exception("the discount is not an existing discount")
        DiscountsInStoreModel.objects.get(storeID=self.__model, discountID=discount_model).delete()
        return True

    def getAllDiscounts(self):
        # self.__discounts: {int: IDiscount} = {}
        discounts = {}
        discount_models = DiscountsInStoreModel.objects.filter(storeID=self.__model)
        for d in discount_models:
            discount = self._buildDiscount(d.discountID)
            discounts[discount.getDiscountId()] = discount
        return discounts

    def getAllRules(self):
        rules = {}
        rule_models = RulesInStoreModel.objects.filter(storeID=self.__model)
        for r in rule_models:
            rule = self._buildRule(r.discountID)
            rules[rule.getRuleId()] = rule
        return rules

    def hasDiscountPermission(self, user):
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        return permissions.first().discount

    def addSimpleRule(self, user, dId, rule: IRule):
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.first().discount:
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        if rule.getRuleKind() == 'Discount':
            discount_model = DiscountModel.objects.get(discountID=dId)
            discount = self._buildDiscount(discount_model)
            if discount is None:
                raise Exception("discount does not exists")
            discount.addSimpleRuleDiscount(rule)
        elif rule.getRuleKind() == 'Purchase':
            RulesInStoreModel.objects.get_or_create(storeID=self.__model, ruleID=rule.getModel())
        else:
            raise Exception("rule kind is illegal")

    def addCompositeRule(self, user, dId, ruleId, rId1, rId2, ruleType, ruleKind):    ###NEED TO CHANGE THIS
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        with self.__discountsLock:
            if ruleKind == 1:
                discount: IDiscount = self.__discounts.get(dId)
                if discount is None:
                    raise Exception("discount does not exists")
                return discount.addCompositeRuleDiscount(ruleId, rId1, rId2, ruleType, ruleKind)
            elif ruleKind == 2:
                rule1 = self.__rules.get(rId1)
                rule2 = self.__rules.get(rId2)
                if rule1 is None:
                    raise Exception("rule1 is not an existing discount")
                if rule2 is None:
                    raise Exception("rule2 is not an existing discount")
                newRule = PurchaseRuleComposite(ruleId, rule1, rule2, ruleType, ruleKind)
                self.__rules.pop(rId1)
                self.__rules.pop(rId2)
                self.__rules[ruleId] = newRule
                return newRule
            else:
                raise Exception("rule kind is illegal")

    def removeRule(self, user, dId, rId, ruleKind):
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.first().discount:
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        if ruleKind == 'Discount':
            discount_model = DiscountModel.objects.get(discountID=dId)
            discount = self._buildDiscount(discount_model)
            if discount is None:
                raise Exception("discount does not exists")
            discount.removeDiscountRule(rId)
        elif ruleKind == 'Purchase':
            rule_model = RuleModel.objects.get(ruleID=rId)
            RulesInStoreModel.objects.get(storeID=self.__model, ruleID=rule_model).delete()
        else:
            raise Exception("rule kind is illegal")

    def removeStore(self):
        self.__model.delete()

    def _buildProduct(self, model):
        return Product(model=model)

    def _buildMember(self, model):
        return m.Member(model=model)

    def _buildBankAccount(self,model):
        return Bank(model.accountNumber, model.branch)

    def _buildAddress(self, model):
        return Address(model=model)

    def _buildStoreTransactions(self, model):
        return StoreTransaction(model=model)

    def _buildDiscount(self, model):
        if model.type == 'Product':
            return ProductDiscount(model)
        if model.type == 'Category':
            return CategoryDiscount(model)
        if model.type == 'Store':
            return StoreDiscount(model)
        if model.type == 'Composite':
            return DiscountComposite(model)

    def _buildRule(self, model):
        if model.rule_class == 'DiscountComposite':
            return DiscountRuleComposite(model)
        if model.rule_class == 'Price':
            return PriceRule(model)
        if model.rule_class == 'PurchaseComposite':
            return PurchaseRuleComposite(model)
        if model.rule_class == 'Quantity':
            return QuantityRule(model)
        if model.rule_class == 'Weight':
            return WeightRule(model)

