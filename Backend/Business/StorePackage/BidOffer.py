from typing import Dict

from Backend.Business.Notifications.NotificationHandler import NotificationHandler
from Backend.Business.UserPackage.Member import Member
from Backend.Interfaces.IMember import IMember
from ModelsBackend.models import BidOfferModel, ProductModel, ReceiversOfBid, MemberModel


class BidOffer:

    def __init__(self, user=None, storeID=None, productID=None, newPrice=None, receivers=None, model=None):
        if model is None:
            self.__model = BidOfferModel.objects.get_or_create(user=user.getModel(), storeID=storeID.getModel(),
                                                               productID=ProductModel.objects.get(product_id=productID),
                                                               newPrice=newPrice)[0]
            self.__bID = self.__model.id
            self.__user = user
            self.__storeID = storeID.getStoreId()
            self.__productID = productID
            self.__newPrice = newPrice
            self.__receivers: Dict[IMember: bool] = {}
            self.__active = True
            self.__isAccepted = False
            for receiver in receivers:
                ReceiversOfBid.objects.get_or_create(bid=self.__model, receiver=receiver.getModel())
                self.__receivers[receiver]=False

        else:
            self.__model = model
            self.__bID = self.__model.id
            self.__user = self._buildReceiver(self.__model.user)
            self.__storeID = self.__model.storeID.storeID
            self.__productID = self.__model.productID.product_id
            self.__newPrice = self.__model.newPrice
            self.__active = self.__model.active
            self.__isAccepted = self.__model.isAccepted
            self.__receivers: Dict[IMember: bool] = {}
            receivers_model = ReceiversOfBid.objects.filter(bid=self.__model)
            for receiver_model in receivers_model:
                receiver = self._buildReceiver(receiver_model.receiver)
                self.__receivers[receiver]= receiver_model.accepted


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
        return self.__isAccepted

    def getReceivers(self):
        return self.__receivers

    def acceptOffer(self, user):
        self.__receivers[user] = True
        reciever_model = ReceiversOfBid.objects.get(bid=self.__model, receiver=user.getModel())
        reciever_model.accepted = True
        reciever_model.save()
        check = self.__receivers.values()
        if all(check):
            notification_handler: NotificationHandler = NotificationHandler.getInstance()
            notification_handler.notifyBidAccepted(self.__user, self.__storeID, self.__bID)
            self.__model.isAccepted = True
            self.__model.save()
            self.__isAccepted = True

    def rejectOffer(self):
        self.__active = False
        self.__model.active = False
        self.__model.save()
        notification_handler: NotificationHandler = NotificationHandler.getInstance()
        notification_handler.notifyBidDeclined(self.__user, self.__storeID, self.__bID)
        self.__model.delete()

    def offerAlternatePrice(self,user, new_price):
        if new_price < self.__newPrice:
            raise Exception("cant give lower price then the first price!")
        self.__newPrice = new_price
        self.__model.newPrice = new_price
        self.__model.save()
        self.__receivers[self.__user] = False
        self.__receivers[user] = True
        notification_handler: NotificationHandler = NotificationHandler.getInstance()
        notification_handler.notifyBidAlternateOffer(self.__user, self.__storeID, self.__bID)

    def _buildReceiver(self, model):
        return Member(model=model)
