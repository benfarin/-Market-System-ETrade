from Service.DTO import cartDTO, paymentStatusDTO, userTransactionDTO
from typing import Dict


class guestDTO:
    def __init__(self, userId, cart):
        self.__id = userId
        self.__cart: cartDTO = cart

    def getUserID(self):
        return self.__id

    def getCart(self):
        return self.__cart

    def setICart(self, cart):
        self.__cart = cart

    def setUserID(self, uid):
        self.__id = uid