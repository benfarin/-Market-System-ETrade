class DeliveryStatus:
    def __init__(self, deliveryId, UserID, storeId, status):
        self.__deliveryId = deliveryId
        self.__UserID = UserID
        self.__storeId = storeId
        self.__status = status

    def getUserID(self):
        return self.__UserID

    def getStatus(self):
        return self.__status

    def getStoreID(self):
        return self.__storeId

    def getDeliveryID(self):
        return self.__deliveryId

    def setStatus(self, status):
        self.__status = status
