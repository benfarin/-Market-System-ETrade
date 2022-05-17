from Business.StorePackage.Bag import Bag
from Service.DTO.ProductDTO import ProductDTO


class BagDTO:

    def __init__(self, bag: Bag):
        self.__storeId = bag.getStoreId()
        self.__products = {}
        for product in bag.getProducts().keys():
            self.__products[ProductDTO(product)] = bag.getProducts().get(product)

    def setStore(self, storeId):
        self.__storeId = storeId

    def getStoreId(self):
        return self.__storeId

    def getProduct(self, productID):
        return self.__products.get(productID)

    def getAllProducts(self):
        return self.__products

    def __str__(self):
        toReturn = "bag" + str(self.__storeId) + ":"
        toReturn += "\n\t\t\t\tproducts: "
        for product in self.__products.keys():
            toReturn += "\n\t\t\t\t\t" + product.printInBag()
            toReturn += "\n\t\t\t\t\t\tquantity: " + str(self.__products.get(product))
        return toReturn

    def getAllProductsAsList(self):
        return self.__products.keys()