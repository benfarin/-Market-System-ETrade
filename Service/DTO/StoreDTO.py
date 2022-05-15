from Business.StorePackage.Store import Store
from Service.DTO.ProductDTO import ProductDTO
from Service.DTO.MemberDTO import MemberDTO
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
        self.__managers = []
        for manager in store.getStoreManagers():
            self.__managers.append(MemberDTO(manager))
        self.__owners = []
        for owner in store.getStoreOwners():
            self.__owners.append(MemberDTO(owner))
        self.__products = {}
        for productId in store.getProducts().keys():
            self.__products[productId] = ProductDTO(store.getProducts().get(productId))
        self.__productsQuantity = store.getProductQuantity()
        self.__transactions = {}
        for tId in store.getTransactionForDTO().values():
            self.__transactions[tId] = storeTransactionDTO(store.getTransactionForDTO().get(tId))
        self.__permissions = {}
        for member in store.getPermissionForDto().keys():
            self.__permissions[member.getMemberName()] = StorePermissionDTO(store.getPermissionForDto().get(member))

    def getAppointerByUserID(self, uid):
        return self.__appointers.get(uid)

    def getProductByPruductID(self, pid):
        return self.__products.get(pid)

    def getTransactionByID(self, tid):
        return self.__transactions.get(tid)

    def getPermissionByUserID(self, uid):
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

    def getProductsAsList(self):
        products_list = []
        for product in self.__products.values():
            products_list.append(ProductDTO(product))
        return products_list

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

    def setTransactionDTO(self, transaction):
        self.__transactions = transaction

    def setPermissionDTO(self, permission):
        self.__permissions = permission

    def getProductsAsList(self):
        products_list = []
        for product in self.__products.values():
            products_list.append(ProductDTO(product))
        return products_list

    def __str__(self):
        toReturn = "store " + str(self.__id) + ":"
        toReturn += "\n\tname: " + self.__name
        toReturn += "\n\tfounder id: " + str(self.__founderId)
        toReturn += "\n\towners:"
        for owner in self.__owners:
            toReturn += "\n\t\t" + owner.getMemberName()
        toReturn += "\n\tmanagers:"
        for manager in self.__managers:
            toReturn += "\n\t\t" + manager.getMemberName()
        toReturn += "\n\tproducts: "
        for product in self.__products:
            toReturn += "\n\t\t" + product.__str__()
            toReturn += "\n\t\t\tquantity: " + self.__productsQuantity.get(product.getProductId())
        toReturn += "\n\ttransactions: "
        for transaction in self.__transactions:
            toReturn += "\n\t\t" + transaction.__str__()
        toReturn += "\n\tpermissions:"
        for member in self.__permissions.keys():
            toReturn += "\n\t\t" + self.__permissions.get(member).__str__()
        return toReturn
