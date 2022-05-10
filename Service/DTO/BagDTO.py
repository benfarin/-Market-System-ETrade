from Business.StorePackage.Bag import Bag
from Service.DTO.ProductDTO import ProductDTO


class BagDTO:

    def __init__(self, bag: Bag):
        self.__storeId = bag.getStoreId()
        self.__products: [int, ProductDTO] = bag.getProducts()
        self.__storeName = bag.getStoreName()

    def setStore(self, storeId):
        self.__storeId = storeId

    def getStoreId(self):
        return self.__storeId

    def getProduct(self, productID):
        return self.__products.get(productID)

    def getAllProducts(self):
        return self.__products

    def getAllProductsAsList(self):
        products = []
        for prodcut in self.__products.values():
            products.append(ProductDTO(prodcut))
        return products



    def getStoreName(self):
        return self.__storeName