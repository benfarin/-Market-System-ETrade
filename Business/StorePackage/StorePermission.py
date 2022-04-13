class StorePermission:
    def __init__(self):
        self.__addProduct = False
        self.__appointManager = False
        self.__appointOwner = False

    def hasPremission_AddProduct(self):
        return self.__addProduct

    def hasPremission_appointManager(self):
        return self.__appointManager

    def hasPremission_appointOwner(self):
        return self.__appointOwner

    def setPremission_AddProduct(self, addProduct):
        self.__addProduct = addProduct

    def setPremission_appointManager(self, appointManager):
        self.__appointManager = appointManager

    def setPremission_appointOwner(self, appointOwner):
        self.__appointOwner = appointOwner
