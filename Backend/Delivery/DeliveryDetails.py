class DeliveryDetails:
    def __init__(self, userID, storeId, name, address):
        self.__userID = userID
        self.__storeID = storeId
        self.__name = name
        self.__address = address

    def getUserID(self):
        return self.__userID

    def getStoreID(self):
        return self.__storeID

    def getName(self):
        return self.__name

    def getAddress(self):
        return self.__address
