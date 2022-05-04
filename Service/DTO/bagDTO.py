from Service.DTO.productDTO import productDTO


class bagDTO:

    def __init__(self, storeId):
        self.__storeId = storeId
        self.__products: [int, productDTO] = {}  # product : quantity

    def setStore(self, storeId):
        self.__storeId = storeId

    def getStoreId(self):
        return self.__storeId

    def getProduct(self, productID):
        return self.__products.get(productID)
