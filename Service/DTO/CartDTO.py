from Business.StorePackage.Cart import Cart
from Service.DTO import BagDTO
from typing import Dict


class CartDTO:
    def __init__(self, cart: Cart):
        self.__userId = cart.getUserId()
        self.__bags: Dict[int, BagDTO] = cart.getAllBags()  # storeId : Bag

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

    def __str__(self):
        toReturn = "cart of user " + str(self.__userId) + " :"
        toReturn += "\n\t\tbags: "
        for bag in self.__bags.values():
            toReturn += "\n\t\t\t" + bag.__str__()
        return toReturn
