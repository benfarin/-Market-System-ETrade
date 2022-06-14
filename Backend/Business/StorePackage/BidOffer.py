from typing import Dict

from Backend.Business.Notifications.NotificationHandler import NotificationHandler
from Backend.Interfaces.IMember import IMember
from ModelsBackend.models import BidOfferModel, ProductModel


class BidOffer:

    def __init__(self, user=None, storeID=None, productID=None, newPrice=None , permissionsGuys=None, model=None):
        if model is None:
            self.__model = BidOfferModel.objects.get_or_create(user=user.getModel(), storeID=storeID.getModel(),
                                                               productID=ProductModel.objects.get(product_id=productID),
                                                               newPrice=newPrice)[0]
            for receiver in permissionsGuys:
                self.__model.permissionsGuys.add(receiver.getModel())
            self.__bID = self.__model.id
            self.__userID = user.getUserID()
            self.__storeID = storeID.getStoreId()
            self.__productID = productID
            self.__newPrice = newPrice
            self.__permissionsGuys: Dict[IMember: bool] = {}
            self.__accepted = 0
            self.__active = True
            for receiver in permissionsGuys:
                self.__permissionsGuys.update({receiver, False})

        else:
            self.__model = model
            self.__bID = self.__model.id
            self.__userID = self.__model.user.userid
            self.__storeID = self.__model.storeID.storeID
            self.__productID = self.__model.productID.product_id
            self.__newPrice = self.__model.newPrice
            self.__permissionsGuys = None
            self.__accepted = self.__model.accepted
            self.__active = self.__model.active

    def get_bID(self):
        return self.__bID


    def acceptOffer(self, userID):
        self.__permissionsGuys[userID] = True
        self.__accepted += 1
        if self.__accepted == len(self.__permissionsGuys):
            notification_handler: NotificationHandler = NotificationHandler.getInstance()
            notification_handler.notifyBidAccepted(self.__userID, self.__storeID, self.__bID)

    def rejectOffer(self):
        self.__active = False
        self.__model.active = False
        self.__model.save()
        notification_handler: NotificationHandler = NotificationHandler.getInstance()
        notification_handler.notifyBidDeclined(self.__userID, self.__storeID, self.__bID)


    def offerAlternatePrice(self, new_price):
        self.__newPrice = new_price
        self.__model.newPrice = new_price
        self.__model.save()
        notification_handler: NotificationHandler = NotificationHandler.getInstance()
        notification_handler.notifyBidAlternateOffer(self.__userID, self.__storeID, self.__bID)








