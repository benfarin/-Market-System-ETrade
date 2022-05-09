from Business.StorePackage.Store import Store
from Service.DTO.ProductDTO import ProductDTO
from Service.DTO.storeTransactionDTO import storeTransactionDTO
from Service.DTO.StorePermissionDTO import StorePermissionDTO
from typing import List
from typing import Dict


class StoreDTO:

    def __init__(self, store: Store):
        self.__id = store.getStoreId()
        self.__name = store.getStoreName()
        self.__founderId = store.getStoreFounderId()
        self.__address = store.getStoreAddress()
        # self.__managers = []  # userId
        # self.__owners = [founderId]  # userId
        self.__products: Dict[int: ProductDTO] = store.getProducts()  # productId : Product
        # self.__productsQuantity = {}  # productId : quantity
        # self.__transactions: Dict[int: storeTransactionDTO] = {}
        # self.__permissions: Dict[str: storePermissionDTO] = {
        #     founderId: storePermissionDTO()}  # UserId : storePermission

    def getAppointerByUserID(self, uid):
        return self.__appointers.get(uid)

    def getProductByPruductID(self,pid):
        return self.__products.get(pid)

    def getTransactionByID(self,tid):
        return self.__transactions.get(tid)

    def getPermissionByUserID(self,uid):
        return self.__permissions.get(uid)

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

    def getStoreAppointers(self):
        return self.__appointers

    def getStoreOwners(self):
        return self.__owners

    def getStoreManagers(self):
        return self.__managers

    def getProducts(self):
        return self.__products

    def getProductQuantity(self):
        return self.__productsQuantity

    def getTransactionDTO(self):
        return self.__transactions

    def getPermissionDTO(self):
        return self.__permissions

    def setStoreId(self, id):
        self.__id = id

    def setStoreName(self, name):
        self.__name = name

    def setStoreFounderId(self, founder):
        self.__founderId = founder

    def setStoreBankAccount(self, bank):
        self.__bankAccount = bank

    def setStoreAddress(self, adress):
        self.__address = adress

    def setStoreAppointers(self, appointers):
        self.__appointers = appointers

    def setStoreOwners(self, owners):
        self.__owners = owners

    def setStoreManagers(self, managers):
        self.__managers = managers

    def setProducts(self, products: ProductDTO):
        self.__products = products

    def setProductQuantity(self, prductQuantity):
        self.__productsQuantity = prductQuantity

    def setTransactionDTO(self,transaction):
        self.__transactions = transaction

    def setPermissionDTO(self, permission):
        self.__permissions = permission
