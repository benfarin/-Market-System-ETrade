import zope
from zope.interface import implements
import os, django

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount
from Backend.Business.Notifications.NotificationHandler import NotificationHandler
from Backend.Business.Rules.RuleCreator import RuleCreator
from Backend.Business.StorePackage.BidOffer import BidOffer
from Backend.Business.StorePackage.Product import Product
import Backend.Business.UserPackage.Member as m
from Backend.Interfaces.IDiscount import IDiscount
from Backend.Interfaces.IRule import IRule

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
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ModelsBackend.models import StoreModel, StoreUserPermissionsModel, ProductModel, \
    ProductsInStoreModel, StoreAppointersModel, TransactionsInStoreModel, StoreTransactionModel, DiscountsInStoreModel, \
    DiscountModel, RulesInStoreModel, RuleModel, DiscountRulesModel, BidOfferModel


@zope.interface.implementer(IStore)
class Store:
    def __init__(self, storeId=None, storeName=None, founder=None, bankAccount=None, address=None, model=None):
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
                                                                purchaseHistoryInformation=True, discount=True, bid=True)[0]

            self.__id = storeId
            self.__name = storeName
            self.__founderId = founder.getUserID()
            self.__bankAccount: Bank = bankAccount
            self.__address: Address = address
            # self.__appointers: Dict[IMember: []] = {}  # Member : Members list
            self.__managers = []  # Members
            self.__owners = [founder]  # Members
            self.__products: Dict[int: IProduct] = {}  # productId : Product
            self.__productsQuantity = {}  # productId : quantity
            self.__transactions: Dict[int: StoreTransaction] = {}
            self.__discounts: {int: IDiscount} = {}
            self.__rules: {int: IRule} = {}
            self.__bids: {int: BidOffer} = {}

            self.__permissions: Dict[IMember: StorePermission] = \
                {founder: StorePermission(self.__model, founder.getUserID())}  # member : storePermission
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
            self.__permissions[founder].setPermission_Bid(True)

        else:
            self.__model = model
            self.__permissions_model = \
                StoreUserPermissionsModel.objects.get_or_create(userID=self.__model.founderId, storeID=self.__model,
                                                                appointManager=True,
                                                                appointOwner=True, closeStore=True,
                                                                stockManagement=True,
                                                                changePermission=True, rolesInformation=True,
                                                                purchaseHistoryInformation=True, discount=True)[0]

            self.__id = self.__model.storeID
            self.__name = self.__model.name
            self.__founderId = self.__model.founderId
            self.__bankAccount: Bank = self._buildBankAccount(self.__model.bankAccount)
            self.__address: Address = self._buildAddress(self.__model.address)
            self.__owners = []
            for owner_model in self.__model.owners.all():
                owner = self._buildMember(owner_model)
                self.__owners.append(owner)
            self.__managers = []
            for manager_model in self.__model.managers.all():
                manager = self._buildMember(manager_model)
                self.__managers.append(manager)
            self.__products: Dict[int: IProduct] = {}
            for prod in ProductsInStoreModel.objects.filter(storeID=self.__model.storeID):  ####MAYBE NEED TO SAVE BEFORE
                product = self._buildProduct(prod.productID)
                self.__products.update({product.getProductId(): product})
            self.__productsQuantity = {}  # productId : quantity
            for prod in ProductsInStoreModel.objects.filter(storeID=self.__model.storeID):
                self.__productsQuantity[prod.productID.product_id] = prod.quantity
            self.__transactions: Dict[int: StoreTransaction] = {}
            for tran in StoreTransactionModel.objects.filter(storeId=self.__model.storeID):
                storeTransaction = self._buildStoreTransactions(tran)
                self.__transactions.update({storeTransaction.getTransactionID(): storeTransaction})
            self.__discounts: {int: IDiscount} = {}
            discount_models = DiscountsInStoreModel.objects.filter(storeID=self.__model)
            for d in discount_models:
                discount = self._buildDiscount(d.discountID)
                self.__discounts[discount.getDiscountId()] = discount
            self.__rules: {int: IRule} = {}
            rule_models = RulesInStoreModel.objects.filter(storeID=self.__model)
            for r in rule_models:
                rule = RuleCreator.getInstance().buildRule(r.ruleID)
                self.__rules[rule.getRuleId()] = rule
            self.__permissions: Dict[IMember: StorePermission] = {}
            store_permissions = StoreUserPermissionsModel.objects.filter(storeID=self.__model)
            for permission_model in store_permissions:
                member = self._buildMember(permission_model.userID)
                permission = self._buildPermission(permission_model)
                self.__permissions.update({member: permission})
            self.__bids: {int: BidOffer} = {}
            bids_models = BidOfferModel.objects.filter(storeID=self.__model)
            for bid_model in bids_models:
                bid = self._buildBid(bid_model)
                self.__bids.update({bid.get_bID(): bid})

        self.__permissionsLock = threading.Lock()
        self.__stockLock = threading.Lock()
        self.__productsLock = threading.Lock()
        self.__rolesLock = threading.Lock()
        self.__transactionLock = threading.Lock()
        self.__discountsLock = threading.Lock()
        self.__notificationHandler : NotificationHandler = NotificationHandler.getInstance()

    def getStoreId(self):
        return self.__id


    def getStoreName(self):
        return self.__name

    def getName(self):
        return self.__name

    def getStoreFounderId(self):
        return self.__founderId

    def getStoreBankAccount(self):
        return self.__bankAccount

    def getStoreAddress(self):
        return self.__address

    def getStoreOwners(self):
        return self.__owners

    def getBids(self):
        return self.__bids

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
                self.__permissions[assignee].setPermission_StockManagement(True)
                assignee_permissions.stockManagement = True
                assignee_permissions.save()


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
                self.__permissions[assignee].setPermission_AppointManager(True)
                assignee_permissions.appointManager = True
                assignee_permissions.save()


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
                self.__permissions[assignee].setPermission_AppointOwner(True)
                assignee_permissions.appointOwner = True
                assignee_permissions.save()


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
                self.__permissions[assignee].setPermission_ChangePermission(True)
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
                self.__permissions[assignee].setPermission_RolesInformation(True)
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
                self.__permissions[assignee].setPermission_PurchaseHistoryInformation(True)
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
                self.__permissions[assignee].setPermission_Discount(True)
                assignee_permissions.discount = True
                assignee_permissions.save()

    def setBidPermission(self, assigner, assignee):
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
                self.__permissions[assignee].setPermission_Bid(True)
                assignee_permissions.bid = True
                assignee_permissions.save()

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

    def hasProduct(self, productId):
        return productId in self.__products.keys()

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
                ProductsInStoreModel.objects.get_or_create(storeID=self.__model, productID=product.getModel(),
                                                           quantity=0)
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
                # self.__productsQuantity[productId] += quantity
                quantity_to_change = ProductsInStoreModel.objects.get(storeID=self.__model,
                                                                      productID=productId)
                self.__productsQuantity[productId] += quantity
                quantity_to_change.quantity += quantity
                quantity_to_change.save()

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
            product_model = ProductModel.objects.get_or_create(product_id=productId)[0]
            product = self._buildProduct(model=product_model)
            product.removeProduct()


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
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store: ", self.__name)
        if not permissions.hasPermission_StockManagement():
            raise PermissionException("User ", user.getUserID(), " doesn't have the permission to change the stock in store: ",
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
        with self.__rolesLock:
            self.__managers.append(assignee)
            self.__model.managers.add(assignee.getModel())
            StoreAppointersModel.objects.get_or_create(storeID=self.__model, assigner=assigner.getModel(),
                                                       assingee=assignee.getModel())

            if not StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=assignee.getModel()).exists():
                StoreUserPermissionsModel(userID=assignee.getModel(), storeID=self.__model).save()

        with self.__permissionsLock:
            if self.__permissions.get(assignee) is None:
                self.__permissions[assignee] = StorePermission(self.__model, assignee.getUserID())
            self.__permissions[assignee].setPermission_PurchaseHistoryInformation(True)
            permission = self.__permissions[assignee].getModel()
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

        with self.__rolesLock:
            self.__owners.append(assignee)
            self.__model.owners.add(assignee.getModel())
            StoreAppointersModel.objects.get_or_create(storeID=self.__model, assigner=assigner.getModel(),
                                                       assingee=assignee.getModel())

            if not StoreUserPermissionsModel.objects.filter(storeID=self.__model, userID=assignee.getModel()).exists():
                StoreUserPermissionsModel(storeID=self.__model, userID=assignee.getModel()).save()

        with self.__permissionsLock:
            if self.__permissions.get(assignee) is None:
                self.__permissions[assignee] = StorePermission(self.__model, assignee.getUserID())
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
        self.__owners.remove(assignee)
        StoreUserPermissionsModel.objects.get(storeID=self.__model, userID=assignee.getModel()).delete()
        for model in StoreModel.owners.through.objects.all():
            if assignee.getModel() == model.membermodel:
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
            TransactionsInStoreModel.objects.get_or_create(storeID=self.__model, transactionID=transaction.getModel())

    def removeTransaction(self, transactionId):
        with self.__transactions:
            if transactionId in self.__transactions.keys():
                self.__transactions.pop(transactionId)
                transaction_model = StoreTransactionModel.objects.get(transactionId=transactionId)
                TransactionsInStoreModel.objects.get(storeID=self.__model, transactionID=transaction_model).delete()

    def getTransaction(self, transactionId):
        if transactionId not in self.__transactions.keys():
            raise TransactionException("in store: ", self.__id, "there is not transaction with Id: ", transactionId)
        self.__transactions.get(transactionId)


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
        with self.__stockLock:
            product_model = ProductModel.objects.get(product_id=productId)
            if self.__products.get(productId) is None:
                raise ProductException("product: ", productId, "cannot be added because it is not in store: ",
                                       self.__id)
            if self.__productsQuantity[productId] < quantity:
                raise ProductException("cannot add a negative quantity to bag")
            quantity_to_change = ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model)
            quantity_to_change.quantity -= quantity
            quantity_to_change.save()
            self.__productsQuantity[productId] -= quantity
            return True

    def removeProductFromBag(self, productId, quantity):  ###NO USE OF THIS FUNCTION - NEED TO DELETE IT?
        with self.__stockLock:
            if productId not in self.__products.keys():
                raise ProductException("product: ", productId, "cannot be remove because it is not in store: ",
                                       self.__id)

            product_model = ProductModel.objects.get(product_id=productId)
            product_to_change = ProductsInStoreModel.objects.get(storeID=self.__model, productID=product_model)
            product_to_change.quantity += quantity
            product_to_change.save()
            self.__productsQuantity[productId] += quantity

    def hasRole(self, user):
        return user in self.getStoreOwners() or user in self.getStoreManagers()

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
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        DiscountsInStoreModel.objects.get_or_create(storeID=self.__model, discountID=discount.getModel())
        self.__discounts[discount.getDiscountId()] = discount

    def addCompositeDiscount(self, user, discountId, dId1, dId2, discountType, decide):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
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
        self.__discounts[discount.getDiscountId()] = discount
        DiscountsInStoreModel.objects.get(storeID=self.__model, discountID=d1.getModel()).delete()
        self.__discounts.pop(d1.getDiscountId())
        DiscountsInStoreModel.objects.get(storeID=self.__model, discountID=d2.getModel()).delete()
        self.__discounts.pop(d2.getDiscountId())
        return discount

    def removeDiscount(self, user, dId):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        if self.__discounts.get(dId) is None:
            raise Exception("the discount is not an existing discount")

        with self.__discountsLock:
            discount = self.__discounts.get(dId)
            self.__discounts.pop(dId)
            discount.remove()
        return True

    def getAllDiscounts(self):
        return self.__discounts

    def getAllRules(self):
        return self.__rules

    def hasDiscountPermission(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        return permissions.hasPermission_Discount()

    def hasBidPermission(self, user):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        return permissions.hasPermission_Bid()

    def addSimpleRule(self, user, dId, rule):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
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
            self.__rules[rule.getRuleId()] = rule
        else:
            raise Exception("rule kind is illegal")

    def addCompositeRule(self, user, dId, ruleId, rId1, rId2, ruleType, ruleKind):  ###NEED TO CHANGE THIS
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
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
            self.__rules[toReturnDiscount.getRuleId()] = toReturnDiscount
            with self.__discountsLock:
                toReturnDiscount.getModel().rule_class = 'PurchaseComposite'
                toReturnDiscount.getModel().save()

            RulesInStoreModel.objects.get(ruleID=rule1model.first()).delete()
            self.__rules.pop(rule1)
            RulesInStoreModel.objects.get(ruleID=rule2model.first()).delete()
            self.__rules.pop(rule2)
        else:
            raise Exception("rule kind is illegal")

        # self.__rules.pop(rId1)
        # self.__rules.pop(rId2)
        # self.__rules[ruleId] = newRule

        return toReturnDiscount

    def removeRule(self, user, dId, rId, ruleKind):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
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
            self.__rules.pop(rule.getRuleId())
            rule.removeRule()
            # RulesInStoreModel.objects.get(storeID=self.__model, ruleID=rule_model).delete()
        else:
            raise Exception("rule kind is illegal")

    def getAllDiscountOfStore(self, user, isComp):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        discounts = []
        for d in self.__discounts.values():
            if isComp and d.isComp():
                discounts.append(d)
            if not isComp and not d.isComp():
                discounts.append(d)
        return discounts

    def getAllPurchaseRulesOfStore(self, user, isComp):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)
        rules = []
        for r in self.__rules.values():
            if isComp and r.isComp():
                rules.append(r)
            if not isComp and not r.isComp():
                rules.append(r)
        return rules

    def openNewBidOffer(self, user, productID, newPrice):
        try:
            receivers = []
            receivers += self.__owners
            for manager in self.__managers:
                if self.hasBidPermission(manager):
                    receivers.append(manager)

            newBid = BidOffer(user, self,productID,newPrice,receivers)
            self.__notificationHandler.notifyForBidOffer(receivers, self.__id, user)
            self.__bids[newBid.get_bID()] =newBid
            return newBid
        except:
            raise Exception("cannot open new bid for product " + str(productID))

    def acceptBidOffer(self, user , bID):
        try:
            bid: BidOffer = self.__bids.get(bID)
            bid.acceptOffer(user)
            return True
        except Exception as e:
            raise Exception("cannot accept bid " + str(bID))

    def rejectOffer(self, bID):
        try:
            bid: BidOffer = self.__bids.get(bID)
            bid.rejectOffer()
            return True
        except:
            raise Exception("cannot accept bid " + str(bID))

    def offerAlternatePrice(self ,user, bID, new_price):
        try:
            bid: BidOffer = self.__bids.get(bID)
            bid.offerAlternatePrice(user,new_price)
            return True
        except:
            raise Exception("cannot accept bid " + str(bID))

    def getAllRulesOfDiscount(self, user, discountId, isComp):
        permissions = self.__permissions.get(user)
        if permissions is None:
            raise PermissionException("User ", user.getUserID(), " doesn't have any permissions is store:", self.__name)
        if not permissions.hasPermission_Discount():
            raise PermissionException("User ", user.getUserID(), " doesn't have the discount permission in store: ",
                                      self.__name)

        discount = self.__discounts[discountId]
        discountRules = discount.getAllDiscountRules()
        rules = []
        for rule in discountRules:
            if isComp and rule.isComp():
                rules.append(rule)
            if not isComp and not rule.isComp():
                rules.append(rule)
        return rules

    def closeStore(self):
        self.__model.is_active = False
        self.__model.save()

    def recreateStore(self):
        self.__model.is_active = True
        self.__model.save()

    def removeStore(self):
        for prod_model in ProductsInStoreModel.objects.filter(storeID= self.__model.storeID):
            model = prod_model.productID
            model.delete()
        StoreTransactionModel.objects.filter(storeId=self.__model.storeID).delete()
        self.__model.owners.remove()
        self.__model.managers.remove()
        self.__removeDiscount()
        self.__model.delete()

    def __send_channel_message(self, group_name, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            '{}'.format(group_name),
            {
                'type': 'channel_message',
                'message': message
            }
        )

    def __removeDiscount(self):
        for discountInStore in DiscountsInStoreModel.objects.filter(storeID=self.__model):
            discount = self._buildDiscount(discountInStore.discountID)
            for ruleInDiscount in DiscountRulesModel.objects.filter(discountID=discount.getModel()):
                rule = RuleCreator.getInstance().buildRule(ruleInDiscount.ruleID)
                rule.removeRule()
            discount.remove()
            self.__discounts.pop(discount.getDiscountId())

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

    def _buildBid(self, model):
        return BidOffer(model=model)

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
