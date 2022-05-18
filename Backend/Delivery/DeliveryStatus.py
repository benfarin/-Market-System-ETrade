class DeliveryStatus:
    def __init__(self, packageID, UserID, storeId, status):
        self.__packageID = packageID
        self.__UserID= UserID
        self.__storeId = storeId
        self.__status = status

    def getUserID(self):
        return self.__UserID
    def getStatus(self):
        return self.__status
    def getStoreID(self):
        return  self.__storeId
    def getPackageID(self):
        return  self.__packageID

    def setStatus(self, status):
        self.status = status

