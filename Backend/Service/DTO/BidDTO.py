from Backend.Business.StorePackage.BidOffer import BidOffer
from Backend.Service.DTO.GuestDTO import GuestDTO
from Backend.Service.DTO.MemberDTO import MemberDTO


class BidDTO:
    def __init__(self, bid: BidOffer):
        self.__bID = bid.get_bID()
        self.__userID = { bid.get_user().userid: bid.get_user_value() }
        self.__storeID = bid.get_storeID()
        self.__productID = bid.get_productID()
        self.__newPrice = bid.get_newPrice()
        self.__isAccepted = bid.get_Accepted()
        self.__receivers = {}
        for receiver in bid.getReceivers().keys():
            self.__receivers[MemberDTO(receiver)] = bid.getReceivers().get(receiver)

    def get_bID(self):
        return self.__bID

    def get_userID(self):
        return list(self.__userID.keys())[0]

    def get_storeID(self):
        return self.__storeID

    def get_productID(self):
        return self.__productID

    def get_newPrice(self):
        return self.__newPrice

    def get_Accepted(self):
        return self.__isAccepted

    def get_receivers(self):
        return self.__receivers

    def getUserStatus(self):
        return self.__userID

    def isOfferedAlternatePrice(self):
        user_obj  = list(self.__userID.keys())[0]
        return not self.__userID[user_obj]


    def __str__(self):
        toReturn = "bid: "
        toReturn += "\n\t\tbid id: " + str(self.__bID)
        toReturn += "\n\t\tuser id: " + str(self.__userID)
        toReturn += "\n\t\tstore id: " + str(self.__storeID)
        toReturn += "\n\t\tproduct id: " + str(self.__productID)
        toReturn += "\n\t\tnew price: " + str(self.__newPrice)
        toReturn += "\n\t\tis accepted: " + str(self.__isAccepted)
        return toReturn




