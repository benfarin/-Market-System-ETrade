from typing import Dict

from Backend.Business.Notifications.NotificationHandler import NotificationHandler
from Backend.Business.UserPackage.Member import Member
from Backend.Interfaces.IMember import IMember
from ModelsBackend.models import BidOfferModel, ProductModel


class BidOffer:

    def __init__(self, user=None, storeID=None, productID=None, newPrice=None, receivers=None, model=None):
        if model is None:
            self.__model = BidOfferModel.objects.get_or_create(user=user.getModel(), storeID=storeID.getModel(),
                                                               productID=ProductModel.objects.get(product_id=productID),
                                                               newPrice=newPrice)[0]
            for receiver in receivers:
                self.__model.permissionsGuys.add(receiver.getModel())
            self.__bID = self.__model.id
            self.__user = user
            self.__storeID = storeID.getStoreId()
            self.__productID = productID
            self.__newPrice = newPrice
            self.__receivers: Dict[IMember: bool] = {}
            self.__accepted = 0
            self.__active = True
            for receiver in receivers:
                self.__receivers.update({receiver, False})

        else:
            self.__model = model
            self.__bID = self.__model.id
            self.__userID = self.__model.user.userid
            self.__storeID = self.__model.storeID.storeID
            self.__productID = self.__model.productID.product_id
            self.__newPrice = self.__model.newPrice
            self.__accepted = self.__model.accepted
            self.__active = self.__model.active
            self.__receivers: Dict[IMember: bool] = {}
            receivers_model = self.__model.permissionsGuys.through.objects.all()
            for receiver_model in receivers_model:
                receiver = self._buildReceiver(receiver_model)
                self.__receivers.update({receiver, False})


    def get_bID(self):
        return self.__bID

    def get_user(self):
        return self.__user

    def get_storeID(self):
        return self.__storeID

    def get_productID(self):
        return self.__productID

    def get_newPrice(self):
        return self.__newPrice

    def get_Accepted(self):
        return self.__accepted

    def acceptOffer(self, userID):
        self.__receivers[userID] = True
        self.__accepted += 1
        if self.__accepted == len(self.__receivers):
            notification_handler: NotificationHandler = NotificationHandler.getInstance()
            notification_handler.notifyBidAccepted(self.__user.getUserID(), self.__storeID, self.__bID)
            self.__user.addBidProductToCart(self.__productID)

    def rejectOffer(self):
        self.__active = False
        self.__model.active = False
        self.__model.save()
        notification_handler: NotificationHandler = NotificationHandler.getInstance()
        notification_handler.notifyBidDeclined(self.__user.getUserID(), self.__storeID, self.__bID)

    def offerAlternatePrice(self, new_price):
        self.__newPrice = new_price
        self.__model.newPrice = new_price
        self.__model.save()
        notification_handler: NotificationHandler = NotificationHandler.getInstance()
        notification_handler.notifyBidAlternateOffer(self.__user.getUserID(), self.__storeID, self.__bID)

    def _buildReceiver(self, model):
        return Member(model)
