from Service.DTO import bagDTO
from typing import Dict


class cartDTO:
    def __init__(self, userId, bags):
        self.__userId = userId
        self.__bags: Dict[int, bagDTO] = bags  # storeId : Bag

    def getUserId(self):
        return self.__userId

    def getAllBags(self):
        return self.__bags

    def setUserID(self, uid):
        self.__userId = uid

    def setBags(self, bags):
        self.__bags = bags

    def getBagByStoreID(self, storeid):
        return self.__bags.get(storeid)
