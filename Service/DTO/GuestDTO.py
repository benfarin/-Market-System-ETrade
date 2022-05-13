from Business.UserPackage.Guest import Guest
from Service.DTO import CartDTO, PaymentStatusDTO, userTransactionDTO
from typing import Dict


class GuestDTO:
    def __init__(self, guest: Guest):
        self.__id = guest.getUserID()
        self.__cart: CartDTO = guest.getCart()

    def getUserID(self):
        return self.__id

    def getCart(self):
        return self.__cart

    def setICart(self, cart):
        self.__cart = cart

    def setUserID(self, uid):
        self.__id = uid

    def __str__(self):
        toReturn = "guest:"
        toReturn += "\n\tuserId: " + str(self.__id)
        return toReturn + self.__cart.__str__()
