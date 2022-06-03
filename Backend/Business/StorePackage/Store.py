import zope
from zope.interface import implements
import os, django

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount
from Backend.Business.Rules.RuleCreator import RuleCreator
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
from Backend.Interfaces.IStore import IStore
from Backend.Business.StorePackage.StorePermission import StorePermission
from Backend.Business.Transactions.StoreTransaction import StoreTransaction
from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from typing import Dict
import threading
from notifications.signals import notify

from ModelsBackend.models import StoreModel, StoreUserPermissionsModel, ProductModel, \
    ProductsInStoreModel, StoreAppointersModel, TransactionsInStoreModel, StoreTransactionModel, DiscountsInStoreModel, \
    DiscountModel, RulesInStoreModel, RuleModel, DiscountRulesModel


@zope.interface.implementer(IStore)
class Store:

    def __init__(self, storeId=None, storeName=None, founder=None, bankAccount=None, address=None, model=None):
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

        if model is None:
            self.__model = \
            StoreModel.objects.get_or_create(storeID=storeId, name=storeName, founderId=founder.getModel(),
                                             bankAccount=bankAccount.getModel(), address=address.getModel())[0]
            self.__model.owners.add(founder.getModel())

            self.__permissions_model = \
                StoreUserPermissionsModel.objects.get_or_create(userID=founder.getModel(), storeID=self.__model,
                                                                appointManager=True,
                                                                appointOwner=True, closeStore=True,
                                                                stockManagement=True,
                                                                changePermission=True, rolesInformation=True,
                                                                purchaseHistoryInformation=True, discount=True)[0]
        else:
            self.__model = model
            self.__permissions_model = \
                StoreUserPermissionsModel.objects.get_or_create(userID=self.__model.founderId, storeID=self.__model,
                                                                appointManager=True,
                                                                appointOwner=True, closeStore=True,
                                                                stockManagement=True,
                                                                changePermission=True, rolesInformation=True,
                                                                purchaseHistoryInformation=True, discount=True)[0]

        self.__permissionsLock = threading.Lock()
        self.__stockLock = threading.Lock()
        self.__productsLock = threading.Lock()
        self.__rolesLock = threading.Lock()
        self.__transactionLock = threading.Lock()
        self.__discountsLock = threading.Lock()

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

    def getStoreId(self):
        return self.__model.storeID

    def getStoreName(self):
        return self.__model.name

    def getStoreFounderId(self):
        return self.__model.founderId.userid

    def getStoreBankAccount(self):
        return self._buildBankAccount(self.__model.bankAccount)

    def getStoreAddress(self):
        return self._buildAddress(self.__model.address)

    def getStoreOwners(self):
        owners = []
        for owner_model in self.__model.owners.all():
            owner = self._buildMember(owner_model)
            owners.append(owner)
        return owners

    def getStoreManagers(self):
        managers = []
        for manager_model in self.__model.managers.all():
            manager = self._buildMember(manager_model)
            managers.append(manager)
        return managers

    def getProducts(self):
        products: Dict[int: IProduct] = {}
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model.storeID):
            product = self._buildProduct(prod.productID)
            products.update({product.getProductId(): product})
        return products

    def getProductQuantity(self):
        productsQuantity = {}
        for prod in ProductsInStoreModel.objects.filter(storeID=self.__model.storeID):
            productsQuantity[prod.productID.product_id] = prod.quantity
        return productsQuantity

    def getTransactionForDTO(self):
        # self.__transactions: Dict[int: StoreTransaction] = {}
        transactions: Dict[int: StoreTransaction] = {}
        for tran in StoreTransactionModel.objects.filter(storeId=self.__model.storeID):
            storeTransaction = self._buildStoreTransactions(tran)
            transactions.update({storeTransaction.getTransactionID(): storeTransaction})
        return transactions

    def getPermissionForDto(self):
        # self.__permissions: Dict[IMember: StorePermission] = {}
        permissions: Dict[IMember: StorePermission] = {}
        for per in StoreUserPermissionsModel.objects.filter(storeID=self.__model):
            permission = self._buildPermission(per)
            member = self._buildMember(per.userID)
            permissions.update({member: permission})
        return permissions

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
            with self.__permissionsLock:
                assignee_permissions = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(),
                                                                             storeID=self.__model)
                assignee_permissions.stockManagement = True
                assignee_permissions.save()
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
            with self.__permissionsLock:
                assignee_permissions = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(),
                                                                             storeID=self.__model)
                assignee_permissions.appointManagera = True
                assignee_permissions.save()
            # with self.__permissionsLock:
            #     self.__permissions[assignee].setPermission_AppointManager(True)

    def setAppointOwnerPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreOwners():
                raise PermissionException("only owner can assign new owners")
            self.__haveAllPermissions(assigner, assignee)
            if assigner not in self.getStoreOwners():
                raise PermissionException("only owners can assign owners")
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                assignee_permissions = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(),
                                                                             storeID=self.__model)
                assignee_permissions.appointOwner = True
                assignee_permissions.save()
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
            with self.__permissionsLock:
                assignee_permissions = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(),
                                                                             storeID=self.__model)
                assignee_permissions.changePermission = True
                assignee_permissions.save()

    def setRolesInformationPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                assignee_permissions = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(),
                                                                             storeID=self.__model)
                assignee_permissions.rolesInformation = True
                assignee_permissions.save()

    def setPurchaseHistoryInformationPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                assignee_permissions = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(),
                                                                             storeID=self.__model)
                assignee_permissions.purchaseHistoryInformation = True
                assignee_permissions.save()

    def setDiscountPermission(self, assigner, assignee):
        try:
            if assignee not in self.getStoreManagers() and assignee not in self.getStoreOwners():
                raise PermissionException("cannot give a permission to member how is not manager or owner")
            self.__haveAllPermissions(assigner, assignee)
        except Exception as e:
            raise Exception(e)
        else:
            with self.__permissionsLock:
                assignee_permissions = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(),
                                                                             storeID=self.__model)
                assignee_permissions.discount = True
                assignee_permissions.save()

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
        if not StoreAppointersModel.objects.filter(assigner=assigner.getModel(), assingee=assignee.getModel(),
                                                   storeID=self.__model).exists():
            raise PermissionException("User ", assigner.getUserID(), "cannot change the permissions of user: ",
                                      assignee.getUserID(), " because he didn't assign him")

    def hasProduct(self, productId):
        try:
            with self.__stockLock:
                product = ProductModel.objects.get(product_id=productId)
                return ProductsInStoreModel.objects.get(storeID=self.__model, productID=product).quantity > 0
        except:
            return False

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
            if not ProductsInStoreModel.objects.filter(storeID=self.__model, productID=productId).exists():
                raise ProductException("cannot add quantity to a product who doesn't exist, in store: " + self.__name)
            if quantity <= 0:
                raise ProductException("cannot add a non-positive quantity")
        except Exception as e:
            raise Exception(e)
        else:
            with self.__stockLock:
                # self.__productsQuantity[productId] += quantity
                quantity_to_change = ProductsInStoreModel.objects.get(storeID=self.__model,
                                                                      productID=productId)
                quantity_to_change.quantity += quantity
                quantity_to_change.save()

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
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store: ",
                                      self.__name)
        if not permissions.first().stockManagement:
            raise PermissionException("User ", user.getUserID(),
                                      " doesn't have the permission to change the stock in store: ",
                                      self.__name)

    def appointManagerToStore(self, assigner, assignee):
        permissions = StoreUserPermissionsModel.objects.filter(userID=assigner.getModel(), storeID=self.__model)
        if assigner == assignee:
            raise PermissionException("User: ", assignee.getUserID(), " cannot assign himself to manager")
        if not permissions.exists():
            raise PermissionException("User ", assigner.getUserID(), " doesn't have any permissions is store:",
                                      self.__name)
        if not permissions.first().appointManager:
            raise PermissionException("User ", assigner.getUserID(),
                                      " doesn't have the permission - appoint manager in store: ",
                                      self.__name)
        is_assigner_in_owners = StoreModel.objects.filter(storeID=self.__model.storeID, owners=assigner.getModel())
        is_assignee_in_managers = StoreModel.objects.filter(storeID=self.__model.storeID, managers=assignee.getModel())
        if not is_assigner_in_owners.exists():
            raise PermissionException("User ", assigner.getUserID(), "cannot add manager to store: ", self.__name,
                                      "because he is not a store owner")
        # this constrains is also covert the constrains that for each manager there is 1 assigner
        if is_assignee_in_managers.exists():
            raise Exception("User ", assignee.getUserID(), "is all ready a manger in store: ", self.__name)
        # to avoid circularity

        if StoreAppointersModel.objects.filter(assigner=assignee.getModel()).exists() \
                and StoreAppointersModel.objects.filter(assigner=assigner.getModel(),
                                                        assingee=assigner.getModel()).exists():
            raise PermissionException("User ", assignee.getUserID(),
                                      "cannot assign manager to hwo made him owner in store: ",
                                      self.__name)

        self.__model.managers.add(assignee.getModel())
        StoreAppointersModel.objects.get_or_create(storeID=self.__model, assigner=assigner.getModel(),
                                                   assingee=assignee.getModel())

        if not StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=assignee.getModel()).exists():
            StoreUserPermissionsModel(userID=assignee.getModel(), storeID=self.__model).save()

        with self.__permissionsLock:
            permission = StoreUserPermissionsModel.objects.get(userID=assignee.getModel(), storeID=self.__model)
            permission.purchaseHistoryInformation = True
            permission.save()

    def appointOwnerToStore(self, assigner, assignee):
        permissions = StoreUserPermissionsModel.objects.filter(userID=assigner.getModel(), storeID=self.__model)
        if assigner == assignee:
            raise PermissionException("User: ", assignee.getUserID(), " cannot assign himself to manager")
        if not permissions.exists():
            raise PermissionException("User ", assigner.getUserID(), " doesn't have any permissions is store:",
                                      str(self.__id))
        if not permissions.first().appointOwner:
            raise PermissionException("User ", assigner.getUserID(),
                                      " doesn't have the permission - appoint owner in store: ",
                                      self.__name)
        is_assigner_in_owners = StoreModel.objects.filter(storeID=self.__model.storeID, owners=assigner.getModel())
        # managers = StoreModel.objects.filter(storeID=self.__model.storeID, managers=assigner.getModel())
        if not is_assigner_in_owners.exists():
            raise PermissionException("User ", assigner.getUserID(), "cannot add manager to store: ", self.__name,
                                      "because he is not a store owner")
        # this constrains is also covert the constrains that for each owner there is 1 assigner
        is_assignee_in_owners = StoreModel.objects.filter(storeID=self.__model.storeID, owners=assignee.getModel())
        if is_assignee_in_owners.exists():
            raise Exception("User ", assignee.getUserID(), "is all ready a owner in store: ", self.__name)
            # to avoid circularity

        if StoreAppointersModel.objects.filter(assigner=assignee.getModel()).exists() \
                and StoreAppointersModel.objects.filter(assigner=assigner.getModel(),
                                                        assingee=assigner.getModel()).exists():
            raise PermissionException("User ", assignee.getUserID(),
                                      "cannot assign manager to hwo made him owner in store: ",
                                      self.__name)

        self.__model.owners.add(assignee.getModel())
        StoreAppointersModel.objects.get_or_create(storeID=self.__model, assigner=assigner.getModel(),
                                                   assingee=assignee.getModel())

        if not StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=assignee.getModel()).exists():
            StoreUserPermissionsModel(storeID=self.__model, userID=assignee.getModel()).save()

        with self.__permissionsLock:
            assignee_permissions = StoreUserPermissionsModel.objects.get(storeID=self.__model,
                                                                         userID=assignee.getModel())
            assignee_permissions.stockManagement = True
            assignee_permissions.save()
            assignee_permissions.appointManager = True
            assignee_permissions.save()
            assignee_permissions.appointOwner = True
            assignee_permissions.save()
            assignee_permissions.changePermission = True
            assignee_permissions.save()
            assignee_permissions.rolesInformation = True
            assignee_permissions.save()
            assignee_permissions.purchaseHistoryInformation = True
            assignee_permissions.save()
            assignee_permissions.discount = True
            assignee_permissions.save()

    # if the owner was also a manager, need to give the assignee all his permission from the start.
    def removeStoreOwner(self, assigner, assignee):
        if assigner not in self.getStoreOwners():
            raise Exception(
                "user: " + str(assigner.getUserID()) + "is not an owner in store: " + str(self.__model.name))
        if assignee not in self.getStoreOwners():
            raise Exception(
                "user: " + str(assignee.getUserID()) + "is not an owner in store: " + str(self.__model.name))
        if not StoreAppointersModel.objects.filter(storeID=self.__model, assigner=assigner.getModel(),
                                                   assingee=assignee.getModel()).exists():
            raise Exception("user: " + str(assigner.getUserID()) + "cannot remove the user: " +
                            str(assignee.getUserID() + "because he is not the one that appoint him"))

        assignees_of_assignee = StoreAppointersModel.objects.filter(storeID=self.__model, assigner=assignee.getModel())
        if assignees_of_assignee.exists():
            for toRemoveOwner in assignees_of_assignee:
                # in the future we need here to split to remove owner/manager - 4.8
                # they didn't asked us yet to implement.
                to_remove = self._buildMember(toRemoveOwner.assingee)
                self.removeStoreOwner(assignee, to_remove)
        StoreUserPermissionsModel.objects.get(storeID=self.__model, userID=assignee.getModel()).delete()
        for model in StoreModel.objects.filter(storeID=self.__model.storeID, owners=assignee.getModel()):
            if assignee.getModel() == model:
                model.delete()
        StoreAppointersModel.objects.get(storeID=self.__model, assigner=assigner.getModel(),
                                         assingee=assignee.getModel()).delete()

    # print all permission in store - will be deleted this version
    def PrintRolesInformation(self, user):  ####NEED TO CHANGE THIS + NO USE OF THIS FUNCTION - MAYBE DELETE IT?
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
        return permissions.first()

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

    def getName(self):
        return self.__model.name

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

    def getTransactionHistory(self, user):  ###NEED TO CHANGE THIS + NO USE OF THIS FUNCTION - MAYBE DELETE IT?
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

    def addProductToBag(self, productId, quantity):
        product_model = ProductModel.objects.get(product_id=productId)
        if not ProductsInStoreModel.objects.filter(storeID=self.__model, productID=product_model).exists():
            raise ProductException("product: ", productId, "cannot be added because he is not in store: ", self.__id)
        if ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model).quantity < quantity:
            raise ProductException("cannot add a negative quantity to bag")
        else:
            with self.__stockLock:
                quantity_to_change = ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model)
                quantity_to_change.quantity -= quantity
                quantity_to_change.save()
                return True

    def removeProductFromBag(self, productId, quantity):  ###NO USE OF THIS FUNCTION - NEED TO DELETE IT?
        if not ProductModel.objects.filter(product_id=productId).exists():
            raise ProductException("product: ", productId, "cannot be remove because he is not in store: ", self.__id)
        with self.__stockLock:
            product_model = ProductModel.objects.get(product_id=productId)
            product_to_change = ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model)
            product_to_change.quantity += quantity
            product_to_change.save()

    def hasRole(self, user):
        return user in self.getStoreOwners() or user in self.getStoreManagers()

    def getTransactionsForSystemManager(self):  ###NEED TO CHANGE THIS + NO USE OF THIS FUNCTION - MAYBE DELETE IT?
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

    def addCompositeDiscount(self, user, discountId, dId1, dId2, discountType, decide):  ###NEED TO CHANGE THIS
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.first().discount:
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        d1_model = DiscountModel.objects.filter(discountID=dId1)
        d2_model = DiscountModel.objects.filter(discountID=dId2)
        if not d1_model.exists():
            raise Exception("discount1 is not an existing discount")
        if not d2_model.exists():
            raise Exception("discount1 is not an existing discount")
        d1 = self._buildDiscount(d1_model.first())
        d2 = self._buildDiscount(d2_model.first())

        # with self.__discountsLock:
        #     self.__discounts[discount.getDiscountId()] = discount
        #     self.__discounts.pop(dId1)
        #     self.__discounts.pop(dId2)
        discount = DiscountComposite(discountId, d1, d2, discountType, decide)
        DiscountsInStoreModel.objects.get_or_create(storeID=self.__model, discountID=discount.getModel())
        DiscountsInStoreModel.objects.get(storeID=self.__model, discountID=d1.getModel()).delete()
        DiscountsInStoreModel.objects.get(storeID=self.__model, discountID=d2.getModel()).delete()
        return discount

    def removeDiscount(self, user, dId):
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.first().discount:
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        discount_model = DiscountModel.objects.get(discountID=dId)
        discountInStore = DiscountsInStoreModel.objects.filter(storeID=self.__model, discountID=discount_model)
        if not discountInStore.exists():
            raise Exception("the discount is not an existing discount")

        with self.__discountsLock:
            discount = self._buildDiscount(discount_model)
            discount.remove()
        # DiscountsInStoreModel.objects.get(storeID=self.__model, discountID=discount_model).delete()
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
            rule = RuleCreator.getInstance().buildRule(r.ruleID)
            rules[rule.getRuleId()] = rule
        return rules

    def hasDiscountPermission(self, user):
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        return permissions.first().discount

    def addSimpleRule(self, user, dId, rule):
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

    def addCompositeRule(self, user, dId, ruleId, rId1, rId2, ruleType, ruleKind):  ###NEED TO CHANGE THIS
        permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=user.getModel())
        if not permissions.exists():
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.first().discount:
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)

        rule1model = RuleModel.objects.filter(ruleID=rId1)
        rule2model = RuleModel.objects.filter(ruleID=rId2)
        rule1 = RuleCreator.getInstance().buildRule(rule1model.first())
        rule2 = RuleCreator.getInstance().buildRule(rule2model.first())

        if ruleKind == 'Discount':
            discount_model = DiscountModel.objects.filter(discountID=dId)
            if not discount_model.exists():
                raise Exception("discount does not exists")
            discount = self._buildDiscount(discount_model.first())
            toReturnDiscount = discount.addCompositeRuleDiscount(ruleId, rule1.getRuleId(), rule2.getRuleId(), ruleType,
                                                                 ruleKind)
            with self.__discountsLock:
                toReturnDiscount.getModel().rule_class = 'DiscountComposite'
                toReturnDiscount.getModel().save()
        elif ruleKind == 'Purchase':
            if not rule1model.exists():
                raise Exception("rule1 is not an existing discount")
            if not rule2model.exists():
                raise Exception("rule2 is not an existing discount")
            toReturnDiscount = PurchaseRuleComposite(ruleId, rule1, rule2, ruleType, ruleKind)
            RulesInStoreModel.objects.get_or_create(storeID=self.__model, ruleID=toReturnDiscount.getModel())
            with self.__discountsLock:
                toReturnDiscount.getModel().rule_class = 'PurchaseComposite'
                toReturnDiscount.getModel().save()

            RulesInStoreModel.objects.get(ruleID=rule1model.first()).delete()
            RulesInStoreModel.objects.get(ruleID=rule2model.first()).delete()
        else:
            raise Exception("rule kind is illegal")

        # self.__rules.pop(rId1)
        # self.__rules.pop(rId2)
        # self.__rules[ruleId] = newRule

        return toReturnDiscount

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
            rule = RuleCreator.getInstance().buildRule(rule_model)
            rule.removeRule()
            # RulesInStoreModel.objects.get(storeID=self.__model, ruleID=rule_model).delete()
        else:
            raise Exception("rule kind is illegal")

    def closeStore(self):
        self.__model.is_active = False
        self.__model.save()

    def recreateStore(self):
        self.__model.is_active = True
        self.__model.save()

    def removeStore(self):
        StoreTransactionModel.objects.filter(storeId=self.__model.storeID).delete()
        self.__model.owners.remove()
        self.__model.managers.remove()
        self.__removeDiscount()
        self.__model.delete()

    def __removeDiscount(self):
        for discountInStore in DiscountsInStoreModel.objects.filter(storeID=self.__model):
            discount = self._buildDiscount(discountInStore.discountID)
            for ruleInDiscount in DiscountRulesModel.objects.filter(discountID=discount.getModel()):
                rule = RuleCreator.getInstance().buildRule(ruleInDiscount.ruleID)
                rule.removeRule()
            discount.remove()

    def _buildProduct(self, model):
        return Product(model=model)

    def _buildMember(self, model):
        return m.Member(model=model)

    def _buildBankAccount(self, model):
        return Bank(model.accountNumber, model.branch)

    def _buildAddress(self, model):
        return Address(model=model)

    def _buildStoreTransactions(self, model):
        return StoreTransaction(model=model)

    def _buildDiscount(self, model):
        if model.type == 'Product':
            return ProductDiscount(model=model)
        if model.type == 'Category':
            return CategoryDiscount(model=model)
        if model.type == 'Store':
            return StoreDiscount(model=model)
        if model.type == 'Composite':
            return DiscountComposite(model=model)

    def _buildPermission(self, model):
        return StorePermission(model=model)

    def getModel(self):
        return self.__model

    def __eq__(self, other):
        return isinstance(other, Store) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__model.storeID)
