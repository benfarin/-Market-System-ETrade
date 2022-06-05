import uuid
import django, os


from django.db.models import Max
import zope
import Backend.Business.StorePackage.Store as s
from Backend.Exceptions.CustomExceptions import NotOnlineException, ProductException, QuantityException, \
    EmptyCartException, PaymentException, NoSuchStoreException, NotFounderException
from Backend.Interfaces.IMarket import IMarket
from Backend.Interfaces.IStore import IStore
from Backend.Interfaces.IMember import IMember
from Backend.Interfaces.IUser import IUser
from Backend.Payment.PaymentStatus import PaymentStatus
from Backend.Business.Transactions.TransactionHistory import TransactionHistory
from Backend.Payment.PaymentDetails import PaymentDetails
from Backend.Payment.paymentlmpl import Paymentlmpl
from Backend.Business.Transactions.StoreTransaction import StoreTransaction
from Backend.Business.Transactions.UserTransaction import UserTransaction
from zope.interface import implements
from typing import Dict
import threading



from ModelsBackend.models import StoreModel, StoreTransactionModel, UserTransactionModel


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
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
        django.setup()
        """ Virtually private constructor. """
        self.__stores = None  # <id,Store> should check how to initial all the stores into dictionary
        self.__removedStores = None
        self.__globalStore = None
        self.__storeTransactionIdCounter = None
        self.__userTransactionIdCounter = None

        self.__transactionHistory = TransactionHistory.getInstance()
        self.__storeId_lock = threading.Lock()
        self.__StoreTransactionId_lock = threading.Lock()
        self.__UserTransactionId_lock = threading.Lock()

        if Market.__instance is None:
            Market.__instance = self


    def createStore(self, storeName, user, bank, address):  #TESTED
        self.__initializeStoresDict()
        storeID = self.__getGlobalStoreId()
        newStore = s.Store(storeID, storeName, user, bank, address)
        self.__stores[storeID] = newStore
        return newStore

    def isStoreExists(self, storeId): #TESTED
        self.__initializeStoresDict()
        return storeId in self.__stores.keys()

    def getStore(self, storeId):   #TESTED
        self.__initializeStoresDict()
        if storeId in self.__stores.keys():
            return self.__stores.get(storeId)
        raise NoSuchStoreException("store: " + str(storeId) + " doesnt exists in the market")

    def getUserStores(self, user):
        self.__initializeStoresDict()
        allStores = []
        for store in self.__stores.values():
            if store.hasPermissions(user):
                allStores.append(store)
        return allStores

    def addProductToCart(self, user, storeID, productID, quantity):  # TESTED
        self.__initializeStoresDict()
        try:
            if not self.__stores.get(storeID).hasProduct(productID):
                raise ProductException("The product id " + productID + " not in market!")
            if self.__stores.get(storeID).addProductToBag(productID, quantity):
                product = self.__stores.get(storeID).getProduct(productID)
                user.getCart().addProduct(storeID, product, quantity)
                return True
            else:
                raise QuantityException("The quantity " + str(quantity) + " is not available")
        except Exception as e:
            raise Exception(e)

    def __getStoreByProductID(self, productID):
        self.__initializeStoresDict()
        for store in self.__stores.values():
            if store.hasProduct(productID) is not False:
                return store
        raise ProductException("There no product id :" + productID + " in the market!")

    def addProductToCartWithoutStore(self, user, productID, quantity):  # TESTED
        try:
            self.__initializeStoresDict()
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

    def removeProductFromCart(self, storeID, user, productId):  # TESTED
        try:
            self.__initializeStoresDict()
            quantity = user.getCart().removeProduct(storeID, productId)
            self.__stores.get(storeID).removeProductFromBag(productId, quantity)
            return True
        except Exception as e:
            raise Exception(e)

    def updateProductFromCart(self, user, storeID, productId, quantity):  # UnTested
        try:
            self.__initializeStoresDict()
            if self.__stores.get(storeID).hasProduct(productId):
                raise ProductException("The product id " + productId + " not in market!")
            if quantity > 0:
                return self.addProductToCart(user, storeID, productId, quantity)
            else:
                return self.removeProductFromBag(productId, quantity)
        except Exception as e:
            return e

    def getProductByCategory(self, category):  # TESTED
        self.__initializeStoresDict()
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByCategory(category)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductsByName(self, nameProduct):  # TESTED
        self.__initializeStoresDict()
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByName(nameProduct)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductByKeyWord(self, keyword):  # TESTED
        self.__initializeStoresDict()
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByKeyword(keyword)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductByPriceRange(self, minPrice, highPrice):   # TESTED
        self.__initializeStoresDict()
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByPriceRange(minPrice, highPrice)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getCartSum(self, user):
        self.__initializeStoresDict()
        cart = user.getCart()
        totalAmount = 0.0
        for storeId in cart.getAllProductsByStore().keys():
            discounts = self.__stores.get(storeId).getAllDiscounts()
            storeAmount = cart.calcSumOfBag(storeId, discounts)
            totalAmount += storeAmount
        return totalAmount


    def __checkRules(self, rules, bag):
        for rule in rules.values():
            if not rule.check(bag):
                return False
        return True

    # need to remember that if a user add the product to the cart, then the product is in the stock.
    def purchaseCart(self, user, bank): #TESTED - WORK ALONE
        self.__initializeStoresDict()
        try:
            cart = user.getCart()
            if cart.isEmpty():
                raise EmptyCartException("cannot purchase an empty cart")

            storeFailed = []
            storeTransactions: Dict[int: StoreTransaction] = {}
            totalAmount = 0.0

            for storeId in cart.getAllProductsByStore().keys():  # pay for each store
                bag = cart.getBag(storeId)
                rules = self.__stores.get(storeId).getAllRules()
                isValidPurchase = self.__checkRules(rules, bag)   # check that all the purchase rules are valid
                if not isValidPurchase:
                    break

                storeName = self.__stores.get(storeId).getStoreName()
                storeBank = self.__stores.get(storeId).getStoreBankAccount()
                discounts = self.__stores.get(storeId).getAllDiscounts()
                storeAmount = cart.calcSumOfBag(storeId, discounts)
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
                    storeTransactions[transactionId] = storeTransaction
                    cart.cleanBag(storeId)
                else:
                    storeFailed.append(storeId)

            userPaymentId = Paymentlmpl.getInstance().getPaymentId()
            userTransaction = UserTransaction(user.getUserID(), self.__getUserTransactionId(), storeTransactions,
                                              userPaymentId, totalAmount)
            user.addTransaction(userTransaction)
            # self.__transactionHistory.addUserTransaction(userTransaction)

            # need to think what should we do if some of the payments failed
            if len(storeFailed) == 0:
                return userTransaction
            else:
                raise PaymentException("failed to pay in stores: " + str(storeFailed))

            # here need to add delivary
        except Exception as e:
            raise Exception(e)

    #  actions of roles - role managment
    def appointManagerToStore(self, storeID, assigner, assignee):
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).appointManagerToStore(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assigner, assignee):  # TESTED
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).appointOwnerToStore(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def removeStoreOwner(self, storeID, assigner, assignee):
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).removeStoreOwner(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assigner, assignee):
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).setStockManagementPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setAppointOwnerPermission(self, storeID, assigner, assignee):
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).setAppointOwnerPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assigner, assignee):
        self.__initializeStoresDict()
        self.__removeStoreLock.acquire(False)
        try:
            self.__stores.get(storeID).setChangePermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assigner, assignee):
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).setRolesInformationPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assigner, assignee):
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).setPurchaseHistoryInformationPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setDiscountPermission(self, storeID, assigner, assignee):
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).setDiscountPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def addSimpleDiscount(self,user, storeId, discount):
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeId).addSimpleDiscount(user,discount)
            return True
        except Exception as e:
            raise Exception(e)

    def addCompositeDiscount(self, user,storeId, discountId, dId1, dId2, typeDiscount, decide):
        self.__initializeStoresDict()
        try:
            return self.__stores.get(storeId).addCompositeDiscount(user,discountId, dId1, dId2, typeDiscount, decide)
        except Exception as e:
            raise Exception(e)

    def removeDiscount(self,user,storeId, discountId):
        self.__initializeStoresDict()
        try:
            return self.__stores.get(storeId).removeDiscount(user,discountId)
        except Exception as e:
            raise Exception(e)

    def addProductToStore(self, storeID, user, product):  # TESTED
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).addProductToStore(user, product)
            return True
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, user, productId, quantity):  #TESTED
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).addProductQuantityToStore(user, productId, quantity)
            return True
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, user, productId):  #TESTED
        self.__initializeStoresDict()
        try:
            self.__stores.get(storeID).removeProductFromStore(user, productId)
            return True
        except Exception as e:
            raise Exception(e)

    def getRolesInformation(self, storeID, user):
        self.__initializeStoresDict()
        try:
            return self.__stores.get(storeID).getPermissions(user)
        except Exception as e:
            raise Exception(e)

    def getPurchaseHistoryInformation(self, storeID, user):
        self.__initializeStoresDict()
        try:
            return self.__stores.get(storeID).getTransactionHistory(user)
        except Exception as e:
            raise Exception(e)

    def getStoreByName(self, store_name):  #TESTED
        self.__initializeStoresDict()
        store_collection = []
        store_names = self.__stores.keys()
        for s in store_names:
            if self.__stores.get(s).getName() == store_name:
                store_collection.append(self.__stores.get(s))
        return store_collection

    def getStoreById(self, id_store):  #TESTED
        self.__initializeStoresDict()
        return self.__stores.get(id_store)

    def getUserByName(self, userName):
        return self.__activeUsers.get(userName)

    def getStores(self):
        self.__initializeStoresDict()
        stores = []
        for store in self.__stores.values():
            stores.append(store)
        return stores

    # need to add to the service
    def removeStore(self, storeID, user):  #TESTED
        self.__initializeStoresDict()
        try:
            if self.__stores.get(storeID) is None:
                raise NoSuchStoreException("Store " + str(storeID) + " is not exist in system!")
            founderId = self.__stores.get(storeID).getStoreFounderId()
            if founderId != user.getUserID():
                raise NotFounderException("user: " + user.getUserID() + "is not the founder of store: " + str(storeID))
            self.__stores.get(storeID).closeStore()
            self.__removedStores[storeID] = self.__stores.get(storeID)
            self.__stores.pop(storeID)
            return True
        except Exception as e:
            raise Exception(e)

    def recreateStore(self, storeID, founder):  #TESTED
        self.__initializeStoresDict()
        try:
            if self.__removedStores.get(storeID) is None:
                raise NoSuchStoreException("Store " + str(storeID) + " is not removed from the system")
            founderId = self.__removedStores.get(storeID).getStoreFounderId()
            if founderId != founder.getUserID():
                raise NotFounderException(
                    "user: " + founder.getUserID() + "is not the founder of store: " + str(storeID))
            self.__removedStores.get(storeID).recreateStore()
            self.__stores[storeID] = self.__removedStores.get(storeID)
            self.__removedStores.pop(storeID)
            return True
        except Exception as e:
            raise Exception(e)

    def removeStoreForGood(self, storeID, user):  #TESTED
        self.__initializeStoresDict()
        try:
            if self.__stores.get(storeID) is None:
                raise NoSuchStoreException("Store " + str(storeID) + " is not exist in system!")
            founderId = self.__stores.get(storeID).getStoreFounderId()
            if founderId != user.getUserID():
                raise NotFounderException("user: " + user.getUserID() + "is not the founder of store: " + str(storeID))
            self.__stores.get(storeID).removeStore()
            self.__stores.pop(storeID)
            return True
        except Exception as e:
            raise Exception(e)

    def loginUpdates(self, user):  # we need to check if all the store exist if not we remove all the products from
        self.__initializeStoresDict()
        # the user that get in the system!
        for storeID in user.getCart().getAllBags().keys():
            if self.__stores.get(storeID) is None:
                user.getCart().removeBag(storeID)

    def updateProductPrice(self, user, storeID, productId, mewPrice):
        self.__initializeStoresDict()
        try:
            return self.__stores.get(storeID).updateProductPrice(user, productId, mewPrice)
        except Exception as e:
            raise Exception(e)

    def updateProductName(self, user, storeID, productID, newName):
        self.__initializeStoresDict()
        try:
            return self.__stores.get(storeID).updateProductName(user, productID, newName)
        except Exception as e:
            raise Exception(e)

    def updateProductCategory(self, user, storeID, productID, newCategory):
        self.__initializeStoresDict()
        try:
            return self.__stores.get(storeID).updateProductCategory(user, productID, newCategory)
        except Exception as e:
            raise Exception(e)

    def updateProductWeight(self, user, storeId, productID, newWeight):
        self.__initializeStoresDict()
        try:
            return self.__stores.get(storeId).updateProductWeight(user, productID, newWeight)
        except Exception as e:
            raise Exception(e)

    def updateCart(self, cart1, cart2):
        cart1.updateCart(cart2)

    def hasRole(self, user):
        self.__initializeStoresDict()
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
        self.__initializeStoresDict()
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            return self.__stores.get(storeId).getTransactionsForSystemManager()
        except Exception as e:
            raise Exception(e)

    def hasDiscountPermission(self, user, storeId):
        self.__initializeStoresDict()
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            return self.__stores.get(storeId).hasDiscountPermission(user)
        except Exception as e:
            raise Exception(e)

    def addSimpleRule(self, user, storeId, dId, rule):
        self.__initializeStoresDict()
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            return self.__stores.get(storeId).addSimpleRule(user, dId, rule)
        except Exception as e:
            raise Exception(e)

    def addCompositeRule(self, user, storeId, dId, ruleId, rId1, rId2, ruleType, ruleKind):
        self.__initializeStoresDict()
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            return self.__stores.get(storeId).addCompositeRule(user, dId, ruleId, rId1, rId2, ruleType, ruleKind)
        except Exception as e:
            raise Exception(e)

    def removeRule(self, user, storeId, dId, rId, ruleKind):
        self.__initializeStoresDict()
        try:
            if storeId not in self.__stores.keys():
                raise NoSuchStoreException("store: " + str(storeId) + "does not exists")
            return self.__stores.get(storeId).removeRule(user, dId, rId, ruleKind)
        except Exception as e:
            raise Exception(e)

    def __getGlobalStoreId(self):
        if self.__globalStore is None:
            self.__globalStore = StoreModel.objects.aggregate(Max('storeID'))['storeID__max']
            if self.__globalStore is None:
                self.__globalStore = 0
        with self.__storeId_lock:
            storeId = self.__globalStore
            self.__globalStore += 1
            return storeId

    def __getStoreTransactionId(self):
        if self.__storeTransactionIdCounter is None:
            self.__storeTransactionIdCounter = StoreTransactionModel.objects.aggregate(Max('transactionId'))[
                'transactionId__max']
            if self.__storeTransactionIdCounter is None:
                self.__storeTransactionIdCounter = 0
        with self.__StoreTransactionId_lock:
            stId = self.__storeTransactionIdCounter
            self.__storeTransactionIdCounter += 1
            return stId

    def __getUserTransactionId(self):
        if self.__userTransactionIdCounter is None:
            self.__userTransactionIdCounter = UserTransactionModel.objects.aggregate(Max('transactionId'))[
                'transactionId__max']
            if self.__userTransactionIdCounter is None:
                self.__userTransactionIdCounter = 0
        with self.__UserTransactionId_lock:
            utId = self.__userTransactionIdCounter
            self.__userTransactionIdCounter += 1
            return utId

    def __buildStore(self, model):
        return s.Store(model=model)

    def __initializeStoresDict(self):
        if self.__stores is None:
            self.__stores: Dict[str: IStore] = {}
            if StoreModel.objects.all().exists():
                for store_model in StoreModel.objects.filter(is_active=True):
                    store = self.__buildStore(store_model)
                    self.__stores.update({store.getStoreId(): store})
        if self.__removedStores is None:
            self.__removedStores: Dict[str: IStore] = {}
            for store_model in StoreModel.objects.filter(is_active=False):
                store = self.__buildStore(store_model)
                self.__stores.update({store.getStoreId(): store})

    def resetDict(self):
        self.__stores = None
        self.__removedStores = None






