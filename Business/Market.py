import uuid

from Business.StorePackage.Store import Store
from Business.UserPackage.Guest import Guest
from Business.UserPackage.Member import Member
from interfaces.IMarket import IMarket
from interfaces.IStore import IStore
from Business.UserPackage.User import User
from Business.StorePackage.Product import Product
from Payment.PaymentStatus import PaymentStatus
from Payment.PaymentDetails import PaymentDetails
from Payment.paymentlmpl import Paymentlmpl
from Business.Transactions.StoreTransaction import StoreTransaction
from Business.Transactions.UserTransaction import UserTransaction
from interface import implements
from typing import Dict


class Market(implements(IMarket)):
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
        self.__activeUsers: Dict[
            str, User] = {}  # <name,User> should check how to initial all the activeStores into dictionary
        self.__globalStore = 0
        self._transactionIdCounter = 0
        if Market.__instance is None:
            Market.__instance = self

    def __checkOnlineUser(self, userName):
        if (self.__activeUsers.get(userName)) is None:
            raise Exception("The member " + userName + " not online!")
        else:
            return True

    def createStore(self, storeName, userID, bank, address):  # change test!
        if self.__checkOnlineUser(userID):
            storeID = self.__globalStore + 1
            self.__globalStore += 1
            newStore = Store(storeID, storeName, userID, bank, address)
            self.__stores[storeID] = newStore
            return newStore.getStoreId()
        return None

    def addGuest(self):  # ?
        guest = Guest()
        self.__activeUsers[guest.getUserID()] = guest
        return guest.getUserID()

    def addActiveUser(self, user):
        try:
            self.__activeUsers[user.getUserID()] = user
            return True
        except:
            return False

    #  action of buyers - market managment
    def addProductToCart(self, userID, storeID, productID, quantity):  # Tested
        try:
            if self.__checkOnlineUser(userID) is not None:
                if self.__stores.get(storeID).hasProduct(productID) is None:
                    raise Exception("The product id " + productID + " not in market!")
                if self.__stores.get(storeID).addProductToBag(productID, quantity):
                    product = self.__stores.get(storeID).getProduct(productID)
                    self.__activeUsers.get(userID).getCart().addProduct(storeID, product, quantity)
                    return True
                else:
                    raise Exception("The quantity " + quantity + " is not available")
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self, storeID, userID, productId):  # Tested
        try:
            if self.__activeUsers.get(userID):
                quantity = self.__activeUsers.get(userID).getCart().removeProduct(storeID, productId)
                self.__stores.get(storeID).removeProductFromBag(productId, quantity)
                return True
            else:
                raise Exception("user not online")
        except Exception as e:
            raise Exception(e)

    def updateProductFromCart(self, userID, storeID, productId, quantity):  # UnTested
        try:
            if self.__activeUsers.get(userID):
                if self.__stores.get(storeID).hasProduct(productId):
                    raise Exception("The product id " + productId + " not in market!")
                if quantity > 0:
                    return self.addProductToCart(userID, storeID, productId, quantity)
                else:
                    return self.removeProductFromBag(productId, quantity)
            else:
                raise Exception("user not online")
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
        productsInStores= []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByPriceRange(minPrice, highPrice)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def addTransaction(self, storeID, transaction):
        try:
            self.__stores.get(storeID).addTransaction(transaction)
        except Exception as e:
            raise Exception(e)

    def removeTransaction(self, storeID, transactionId):
        try:
            self.__stores.get(storeID).removeTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def purchaseCart(self, userID, bank):
        try:
            if self.__activeUsers.get(userID) is None:
                raise Exception("member with id " + userID + " is not online!")
            cart = self.__activeUsers.get(userID).getCart()
            if cart.isEmpty():
                raise Exception("cannot purchase an empty cart")

            storeFailed = []
            storeTransactions: Dict[int: StoreTransaction] = {}
            totalAmount = 0.0
            paymentStatuses: Dict[int: PaymentStatus] = {}

            for storeId in cart.getAllProductsByStore().keys():  # pay for each store
                storeBank = self.__stores.get(storeId).getStoreBankAccount()
                storeAmount = cart.calcSumOfBag(storeId)
                totalAmount += storeAmount
                paymentDetails = PaymentDetails(userID, bank, storeBank, storeId, storeAmount)
                paymentStatus = Paymentlmpl.getInstance().createPayment(paymentDetails)
                self.__activeUsers.get(userID).addPaymentStatus(paymentStatus)
                paymentStatuses[paymentStatus.getPaymentId()] = paymentStatus

                if paymentStatus.getStatus() == "payment succeeded":
                    productsInStore = cart.getAllProductsByStore()[storeId]

                    self.__activeUsers.get(userID).addPaymentStatus(paymentStatus)
                    transactionId = self.__getTransactionId()
                    storeTransaction: StoreTransaction = StoreTransaction(storeId, transactionId,
                                                                          paymentStatus.getPaymentId(), productsInStore,
                                                                          storeAmount)
                    self.__stores.get(storeId).addTransaction(storeTransaction)
                    storeTransactions[storeId] = storeTransaction
                else:
                    storeFailed.append(storeId)

            self.__activeUsers.get(userID).addTransaction(
                UserTransaction(userID, self.__getTransactionId(), storeTransactions, paymentStatuses))
            if len(storeFailed) == 0:
                return True
            else:
                raise Exception("failed to pay in stores: " + str(storeFailed))

            # here need to add delivary
        except Exception as e:
            raise Exception(e)

    def cancelPurchaseCart(self, userID, transactionId):
        try:
            if self.__activeUsers.get(userID) is None:
                raise Exception("member with id " + userID + " is not online!")
            user = self.__activeUsers.get(userID)
            userTransaction = user.getTransaction(transactionId)

            for storeId in userTransaction.getStoreTransactions().keys():
                store: Store = self.__stores.get(storeId)
                storeTransaction: StoreTransaction = userTransaction.getStoreTransactions()[storeId]

                for product in storeTransaction.getProduts().keys():
                    quantity = storeTransaction.getProduts()[product]
                    store.addProductQuantityToStore(userID, product.getProductId(), quantity)

                store.removeTransaction(storeTransaction.getTransactionID())

            for paymentStatus in userTransaction.getPaymentStatus():
                user.removePaymentStatus(paymentStatus)

        except Exception as e:
            raise Exception(e)

    #  action of roles - role managment
    def appointManagerToStore(self, storeID, assignerID, assigneeID):  # Tested
        try:
            if self.__activeUsers.get(assignerID) is not None:
                self.__stores.get(storeID).appointManagerToStore(assignerID, assigneeID)
                return True
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assignerID, assigneeID):  # unTested
        try:
            if self.__activeUsers.get(assignerID) is not None:
                self.__stores.get(storeID).appointOwnerToStore(assignerID, assigneeID)
                return True
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assignerID, assigneeID):  # Tested
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setStockManagementPermission(assignerID, assigneeID)
                return True
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID):  # Tested
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setAppointOwnerPermission(assignerID, assigneeID)
                return True
            else:
                raise Exception("member with id " + assignerID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assignerID, assigneeID):
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setChangePermission(assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setRolesInformationPermission(assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            if self.__checkOnlineUser(assignerID) is not None:
                self.__stores.get(storeID).setPurchaseHistoryInformationPermission(assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def addProductToStore(self, storeID, userID, product):  # Tested
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).addProductToStore(userID, product)
                return True
            else:
                raise Exception("member with id " + userID + " is not online!")
        except Exception as e:
            raise Exception(e)

    def updateProductPrice(self, storeID, userID, productId, mewPrice):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).updateProductPrice(userID, productId, mewPrice)
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).addProductQuantityToStore(userID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, userID, productId):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).removeProductFromStore(userID, productId)
        except Exception as e:
            raise Exception(e)

    def printRolesInformation(self, storeID, userID):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).PrintRolesInformation(userID)
        except Exception as e:
            raise Exception(e)

    def printPurchaseHistoryInformation(self, storeID, userID):
        try:
            self.__stores.get(storeID).printPurchaseHistoryInformation(userID)
        except Exception as e:
            raise Exception(e)

    def checkOnlineMember(self, userName):
        if (self.__activeUsers.get(userName)) is None:
            raise Exception("The member " + userName + " not online!")

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

    def getActiveUsers(self):
        return self.__activeUsers

    def __getTransactionId(self):
        tId = self._transactionIdCounter
        self._transactionIdCounter += 1
        return tId


    def removeStore(self, storeID, userID):
        try:
            if self.__activeUsers.get(userID) is None:
                raise Exception("member with id " + userID + " is not online!")
            if self.__stores.get(storeID) is None:
                raise Exception("Store " + storeID + " is not exist in system!")
            for user in self.__activeUsers.values():
                user.getCart().removeBag(storeID)
            self.__stores.pop(storeID)
            return "Store removed succesfully!"
        except Exception as e:
            return e

    def loginUpdates(self,
                     userID):  # we need to check if all the store exist if not we remove all the products from the user that get in the systsem!

        for storeID in self.__activeUsers.get(userID).getCart().getAllBags().keys():
            if self.__stores.get(storeID) is None:
                self.__activeUsers.get(userID).getCart().removeBag(storeID)

    def getCart(self, userID):
        try:
            if self.__activeUsers.get(userID) is None:
                raise Exception("member with id " + userID + " is not online!")
            return self.__activeUsers.get(userID).getCart().printBags()
        except Exception as e:
            raise Exception(e)

    def updateProductName(self, userID, storeID, productID, newName):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).updateProductName(userID, productID, newName)
            else:
                raise Exception("user not logged in!")
        except Exception as e:
            raise Exception(e)

    def updateProductCategory(self, userID, storeID, productID, newCategory):
        try:
            if self.__checkOnlineUser(userID) is not None:
                self.__stores.get(storeID).updateProductCategory(userID, productID, newCategory)
            else:
                raise Exception("user not logged in!")
        except Exception as e:
            raise Exception(e)
