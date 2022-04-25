class DeliveryDetails:
    def __init__(self, userID, storeID, phone,weight,source ,destination):
        self.__userID = userID
        self.__storeId = storeID
        self.__Phone = phone
        self.__weight=weight
        self.__source= source
        self.__destination = destination
    def getUserID(self):
        return self.__userID
    def getPhone(self):
        return self._recieverPhone

    def getStoreID(self):
        return self.__storeId

    def getPhone(self):
        return self.__Phone

    def getWeight(self):
        return self.__weight

    def getSourceAdress(self):
        return self.__source
    def getDestinationAdress(self):
        return  self.__destination
