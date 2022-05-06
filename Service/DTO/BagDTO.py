from Business.StorePackage.Bag import Bag
from Service.DTO.ProductDTO import ProductDTO


class BagDTO:

    def __init__(self, bag: Bag):
        self.__storeId = bag.getStoreId()
        self.__products: [int, ProductDTO] = bag.getProducts()

    def setStore(self, storeId):
        self.__storeId = storeId

    def getStoreId(self):
        return self.__storeId

    def getProduct(self, productID):
        return self.__products.get(productID)

    def getAllProducts(self):
        return self.__products