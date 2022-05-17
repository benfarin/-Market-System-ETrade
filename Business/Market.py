import uuid

import zope

from Business.StorePackage.Store import Store
from Exceptions.CustomExceptions import NotOnlineException, ProductException, QuantityException, \
    EmptyCartException, PaymentException, NoSuchStoreException, NotFounderException
from interfaces.IMarket import IMarket
from interfaces.IStore import IStore
from interfaces.IMember import IMember
from interfaces.IUser import IUser
from Payment.PaymentStatus import PaymentStatus
from Business.Transactions.TransactionHistory import TransactionHistory
from Payment.PaymentDetails import PaymentDetails
from Payment.paymentlmpl import Paymentlmpl
from Business.Transactions.StoreTransaction import StoreTransaction
from Business.Transactions.UserTransaction import UserTransaction
from zope.interface import implements
from typing import Dict
import threading


@zope.interface.implementer(IMarket)
class Market:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Market.__instance is None:
            Market()
        return Market.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__stores: Dict[int, IStore] = {}  # <id,Store> should check how to initial all the stores into dictionary
        self.__transactionHistory = TransactionHistory.getInstance()
        self.__removedStores: Dict[str: IStore] = {}

        self.__globalStore = 0
        self.__storeTransactionIdCounter = 0
        self.__userTransactionIdCounter = 0
        self.__storeId_lock = threading.Lock()
        self.__StoreTransactionId_lock = threading.Lock()
        self.__UserTransactionId_lock = threading.Lock()

        if Market.__instance is None:
            Market.__instance = self

    def createStore(self, storeName, user, bank, address):  # change test!
        storeID = self.__getGlobalStoreId()
        newStore = Store(storeID, storeName, user, bank, address)
        self.__stores[storeID] = newStore
        return newStore

    def isStoreExists(self, storeId):
        return storeId in self.__stores.keys()

    def getStore(self, storeId):
        if storeId in self.__stores.keys():
            return self.__stores.get(storeId)
        raise NoSuchStoreException("store: " + str(storeId) + " doesnt exists in the market")

    def getUserStores(self, user):
        allStores = []
        for store in self.__stores.values():
            if store.hasPermissions(user):
                allStores.append(store)
        return allStores

    def getAllStores(self):
        return self.__stores.values()

    def addProductToCart(self, user, storeID, productID, quantity):  # Tested
        try:
            if self.__stores.get(storeID).hasProduct(productID) is None:
                raise ProductException("The product id " + productID + " not in market!")
            if self.__stores.get(storeID).addProductToBag(productID, quantity):
                product = self.__stores.get(storeID).getProduct(productID)
                user.getCart().addProduct(storeID, product, quantity)
                return True
            else:
                raise QuantityException("The quantity " + quantity + " is not available")
        except Exception as e:
            raise Exception(e)

    def __getStoreByProductID(self, productID):
        for store in self.__stores.values():
            if store.getProductFromStore(productID) is not None:
                return store
        raise ProductException("There no product id :" + productID + " in the market!")

    def addProductToCartWithoutStore(self, user, productID, quantity):  # Tested
        try:
            store = self.__getStoreByProductID(productID)
            if store is not None:
                if self.__stores.get(store.getStoreId()).addProductToBag(productID, quantity):
                    product = self.__stores.get(store.getStoreId()).getProduct(productID)
                    user.getCart().addProduct(store.getStoreId(), product, quantity)
                    return True
                else:
                    raise QuantityException("The quantity " + quantity + " is not available")
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self, storeID, user, productId):  # Tested
        try:
            quantity = user.getCart().removeProduct(storeID, productId)
            self.__stores.get(storeID).removeProductFromBag(productId, quantity)
            return True
        except Exception as e:
            raise Exception(e)

    def updateProductFromCart(self, user, storeID, productId, quantity):  # UnTested
        try:
            if self.__stores.get(storeID).hasProduct(productId):
                raise ProductException("The product id " + productId + " not in market!")
            if quantity > 0:
                return self.addProductToCart(user, storeID, productId, quantity)
            else:
                return self.removeProductFromBag(productId, quantity)
        except Exception as e:
            return e

    def getProductByCategory(self, category):
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByCategory(category)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductsByName(self, nameProduct):
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByName(nameProduct)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductByKeyWord(self, keyword):
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByKeyword(keyword)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductByPriceRange(self, minPrice, highPrice):
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByPriceRange(minPrice, highPrice)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    # need to remember that if a user add the product to the cart, then the product is in the stock.
    def purchaseCart(self, user, bank):
        try:
            cart = user.getCart()
            if cart.isEmpty():
                raise EmptyCartException("cannot purchase an empty cart")

            storeFailed = []
            storeTransactions: Dict[int: StoreTransaction] = {}
            totalAmount = 0.0

            for storeId in cart.getAllProductsByStore().keys():  # pay for each store
                storeName = self.__stores.get(storeId).getStoreName()
                storeBank = self.__stores.get(storeId).getStoreBankAccount()
                storeAmount = cart.calcSumOfBag(storeId)
                totalAmount += storeAmount
                paymentDetails = PaymentDetails(user.getUserID(), bank, storeBank, storeAmount)
                paymentStatus = Paymentlmpl.getInstance().createPayment(paymentDetails)

                if paymentStatus.getStatus() == "payment succeeded":
                    productsInStore = cart.getAllProductsByStore()[storeId]

                    # user.addPaymentStatus(paymentStatus)
                    transactionId = self.__getStoreTransactionId()
                    storeTransaction: StoreTransaction = StoreTransaction(storeId, storeName, transactionId,
                                                                          paymentStatus.getPaymentId(), productsInStore,
                                                                          storeAmount)
                    self.__stores.get(storeId).addTransaction(storeTransaction)
                    self.__transactionHistory.addStoreTransaction(storeTransaction)
                    storeTransactions[storeId] = storeTransaction
                    cart.cleanBag(storeId)
                else:
                    storeFailed.append(storeId)

            userPaymentId = Paymentlmpl.getInstance().getPaymentId()
            userTransaction = UserTransaction(user.getUserID(), self.__getUserTransactionId(), storeTransactions,
                                              userPaymentId, totalAmount)
            user.addTransaction(userTransaction)
            self.__transactionHistory.addUserTransaction(userTransaction)

            # need to think what should we do if some of the payments failed
            if len(storeFailed) == 0:
                return userTransaction
            else:
                raise PaymentException("failed to pay in stores: " + str(storeFailed))

            # here need to add delivary
        except Exception as e:
            raise Exception(e)

    #  actions of roles - role managment
    def appointManagerToStore(self, storeID, assigner, assignee):  # Tested
        try:
            self.__stores.get(storeID).appointManagerToStore(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assigner, assignee):  # unTested
        try:
            self.__stores.get(storeID).appointOwnerToStore(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def removeStoreOwner(self, storeID, assigner, assignee):  # unTested
        try:
            self.__stores.get(storeID).removeStoreOwner(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assigner, assignee):  # Tested
        try:
            self.__stores.get(storeID).setStockManagementPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setAppointOwnerPermission(self, storeID, assigner, assignee):  # Tested
        try:
            self.__stores.get(storeID).setAppointOwnerPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assigner, assignee):
        self.__removeStoreLock.acquire(False)
        try:
            self.__stores.get(storeID).setChangePermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assigner, assignee):
        try:
            self.__stores.get(storeID).setRolesInformationPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assigner, assignee):
        try:
            self.__stores.get(storeID).setPurchaseHistoryInformationPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setDiscountPermission(self, storeID, assigner, assignee):
        try:
            self.__stores.get(storeID).setDiscountPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def addProductToStore(self, storeID, user, product):  # Tested
        try:
            self.__stores.get(storeID).addProductToStore(user, product)
            return True
        except Exception as e:
            raise Exception(e)

    def updateProductPrice(self, storeID, user, productId, mewPrice):
        try:
            self.__stores.get(storeID).updateProductPrice(user, productId, mewPrice)
            return True
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, user, productId, quantity):
        try:
            self.__stores.get(storeID).addProductQuantityToStore(user, productId, quantity)
            return True
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, user, productId):
        try:
            self.__stores.get(storeID).removeProductFromStore(user, productId)
            return True
        except Exception as e:
            raise Exception(e)

    def getRolesInformation(self, storeID, user):
        try:
            return self.__stores.get(storeID).getPermissions(user)
        except Exception as e:
            raise Exception(e)

    def getPurchaseHistoryInformation(self, storeID, user):
        try:
            return self.__stores.get(storeID).getTransactionHistory(user)
        except Exception as e:
            raise Exception(e)

    def getStoreByName(self, store_name):
        store_collection = []
        store_names = self.__stores.keys()
        for s in store_names:
            if self.__stores.get(s).getName() == store_name:
                store_collection.append(self.__stores.get(s))
        return store_collection

    def getStoreById(self, id_store):  # maybe should be private
        return self.__stores.get(id_store)

    def getUserByName(self, userName):
        return self.__activeUsers.get(userName)

    def getStores(self):
        return self.__stores

    # need to add to the service
    def removeStore(self, storeID, user):
        try:
            if self.__stores.get(storeID) is None:
                raise NoSuchStoreException("Store " + str(storeID) + " is not exist in system!")
            founderId = self.__stores.get(storeID).getStoreFounderId()
            if founderId != user.getUserID():
                raise NotFounderException("user: " + user.getUserID() + "is not the founder of store: " + str(storeID))
            self.__removedStores[storeID] = self.__stores.get(storeID)
            self.__stores.pop(storeID)
            return True
        except Exception as e:
            raise Exception(e)

    def recreateStore(self, storeID, founder):
        try:
            if self.__removedStores.get(storeID) is None:
                raise NoSuchStoreException("Store " + str(storeID) + " is not removed from the system")
            founderId = self.__removedStores.get(storeID).getStoreFounderId()
            if founderId != founder.getUserID():
                raise NotFounderException(
                    "user: " + founder.getUserID() + "is not the founder of store: " + str(storeID))
            self.__stores[storeID] = self.__removedStores.get(storeID)
            self.__removedStores.pop(storeID)
            return True
        except Exception as e:
            raise Exception(e)

    def loginUpdates(self, user):  # we need to check if all the store exist if not we remove all the products from
        # the user that get in the system!
        for storeID in user.getCart().getAllBags().keys():
            if self.__stores.get(storeID) is None:
                user.getCart().removeBag(storeID)

    def updateProductName(self, user, storeID, productID, newName):
        try:
            self.__stores.get(storeID).updateProductName(user, productID, newName)
            return True
        except Exception as e:
            raise Exception(e)

    def updateProductCategory(self, user, storeID, productID, newCategory):
        try:
            self.__stores.get(storeID).updateProductCategory(user, productID, newCategory)
            return True
        except Exception as e:
            raise Exception(e)

    def updateProductWeight(self, user, storeId, productID, newWeight):
        try:
            self.__stores.get(storeId).updateProductWeight(user, productID, newWeight)
            return True
        except Exception as e:
            raise Exception(e)

    def updateCart(self, cart1, cart2):
        cart1.updateCart(cart2)

    def hasRole(self, user):
        for store in self.__stores.values():
            if store.hasRole(user):
                return True
        return False

    def getAllStoreTransactions(self):
        try:
            return self.__transactionHistory.getAllStoreTransactions()
        except Exception as e:
            raise Exception(e)

    def getAllUserTransactions(self):
        try:
            return self.__transactionHistory.getAllUserTransactions()
        except Exception as e:
            raise Exception(e)

    def getStoreTransaction(self, transactionId):
        try:
            return self.__transactionHistory.getStoreTransactionById(transactionId)
        except Exception as e:
            raise Exception(e)

    def getUserTransaction(self, transactionId):
        try:
            return self.__transactionHistory.getUserTransactionById(transactionId)
        except Exception as e:
            raise Exception(e)

    def getStoreTransactionByStoreId(self, storeId):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            return self.__stores.get(storeId).getTransactionsForSystemManager()
        except Exception as e:
            raise Exception(e)

    def addDiscount(self, storeId, user, discount):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            self.__stores.get(storeId).addDiscount(user, discount)
        except Exception as e:
            raise Exception(e)

    def removeDiscount(self, storeId, user, discountId):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            self.__stores.get(storeId).removeDiscount(user, discountId)
        except Exception as e:
            raise Exception(e)

    def addConditionDiscountAdd(self, storeId, user, dId, dId1, dId2):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            self.__stores.get(storeId).addConditionDiscountAdd(user, dId, dId1, dId2)
        except Exception as e:
            raise Exception(e)

    def addConditionDiscountMax(self, storeId, user, dId, dId1, dId2):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            self.__stores.get(storeId).addConditionDiscountMax(user, dId, dId1, dId2)
        except Exception as e:
            raise Exception(e)

    def addConditionDiscountXor(self, storeId, user, discountId, dId, pred1, pred2, decide):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            self.__stores.get(storeId).addConditionDiscountXor(user, discountId, dId, pred1, pred2, decide)
        except Exception as e:
            raise Exception(e)

    def addConditionDiscountAnd(self, storeId, user, discountId, dId, pred1, pred2):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            self.__stores.get(storeId).addConditionDiscountAnd(user, discountId, dId, pred1, pred2)
        except Exception as e:
            raise Exception(e)

    def addConditionDiscountOr(self, storeId, user, discountId, dId, pred1, pred2):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            self.__stores.get(storeId).addConditionDiscountOr(user, discountId, dId, pred1, pred2)
        except Exception as e:
            raise Exception(e)

    def hasDiscountPermission(self, user, storeId):
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            return self.__stores.get(storeId).hasDiscountPermission(user)
        except Exception as e:
            raise Exception(e)

    def __getGlobalStoreId(self):
        with self.__storeId_lock:
            storeId = self.__globalStore
            self.__globalStore += 1
            return storeId

    def __getStoreTransactionId(self):
        with self.__StoreTransactionId_lock:
            stId = self.__storeTransactionIdCounter
            self.__storeTransactionIdCounter += 1
            return stId

    def __getUserTransactionId(self):
        with self.__UserTransactionId_lock:
            utId = self.__userTransactionIdCounter
            self.__userTransactionIdCounter += 1
            return utId
