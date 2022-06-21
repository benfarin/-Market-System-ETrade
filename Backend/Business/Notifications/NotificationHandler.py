import json
import os
from typing import Dict

import django
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Backend.Business.Notifications.Notification import Notification
from Backend.Business.UserPackage.Member import Member
from Backend.Business.UserPackage.User import User
from ModelsBackend.models import MemberModel, NotificationModel


class NotificationHandler:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if NotificationHandler.__instance is None:
            NotificationHandler()
        return NotificationHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
        django.setup()

        if NotificationHandler.__instance is None:
            NotificationHandler.__instance = self

    ###ownersDict - who to sent to the message
    ###storeID - for information, so the member(owner) would know in what store the buyer bought
    ###buyer - the user object who bought (for information sake)
    def notifyBoughtFromStore(self, ownersDict, storeID, buyer):
        activeUsers: Dict[str, User] = {}
        for member_model in MemberModel.objects.filter(isLoggedIn=True):
            member = self._buildMember(member_model)
            activeUsers.update({member.getUserID(): member})

        for owner in ownersDict:
            if owner in activeUsers.values():
                self.__send_channel_message(owner.getMemberName(),
                                            "user " + str(buyer.getUserID()) + " bought from store " + str(storeID))
            else:
                model = \
                    NotificationModel.objects.get_or_create(userID=owner.getModel(),
                                                            text="user " + str(buyer.getUserID()) +
                                                                 " bought from store " + str(
                                                                storeID))[0]
                notification = self._buildNotification(model)

    def notifyForBidOffer(self, receivers, storeID, buyer):
        activeUsers: Dict[str, User] = {}
        for member_model in MemberModel.objects.filter(isLoggedIn=True):
            member = self._buildMember(member_model)
            activeUsers.update({member.getUserID(): member})
        for receiver in receivers:
            if receiver in activeUsers.values():
                self.__send_channel_message(receiver.getMemberName(),
                                            "user " + str(
                                                buyer.getUserID()) + " has made new bidding offer for store  " + str(
                                                storeID))
            else:
                model = \
                    NotificationModel.objects.get_or_create(userID=receiver.getModel(),
                                                            text="user " + str(buyer.getUserID()) +
                                                                 " has made new bidding offer for store  " +
                                                                 str(storeID))[0]
                notification = self._buildNotification(model)

    def notifyBidAccepted(self, receiver, storeID, bidID):
        activeUsers: Dict[str, User] = {}
        for member_model in MemberModel.objects.filter(isLoggedIn=True):
            member = self._buildMember(member_model)
            activeUsers.update({str(member.getUserID()): member})
        if receiver in activeUsers.values():
            self.__send_channel_message(receiver.getMemberName(),
                                        "your offer " + str(bidID) + " in store " + str(storeID) +
                                        " has been accepted, the product has been added to your cart")
        else:
            send_model = receiver.getModel()
            model = \
                NotificationModel.objects.get_or_create(userID=send_model,
                                                        text="your offer " + str(bidID) +
                                                             " in store " + str(storeID) +
                                                             " has been accepted, the product has been added to your cart")[0]
            notification = self._buildNotification(model)

    def notifyBidDeclined(self, receiver, storeID, bidID):
        activeUsers: Dict[str, User] = {}
        for member_model in MemberModel.objects.filter(isLoggedIn=True):
            member = self._buildMember(member_model)
            activeUsers.update({member.getUserID(): member})
        if receiver in activeUsers.values():
            self.__send_channel_message(receiver.getMemberName(),
                                        "your offer " + str(bidID) + " in store " + str(storeID) +
                                        " has been declined")
        else:
            model = \
                NotificationModel.objects.get_or_create(userID=receiver.getModel(),
                                                        text="your offer " + str(bidID) + " in store " +
                                                             str(storeID) + " has been declined")[0]
            notification = self._buildNotification(model)

    def notifyBidAlternateOffer(self, receiver, storeID, bidID):
        activeUsers: Dict[str, User] = {}
        for member_model in MemberModel.objects.filter(isLoggedIn=True):
            member = self._buildMember(member_model)
            activeUsers.update({member.getUserID(): member})
        if receiver in activeUsers.values():
            self.__send_channel_message(receiver.getMemberName(),
                                        "your offer " + str(bidID) + " in store " + str(storeID) +
                                        " got alternative offer")
        else:
            model = \
                NotificationModel.objects.get_or_create(userID=receiver.getModel(),
                                                        text="your offer " + str(bidID) + " in store " + str(storeID) +
                                                             " got alternative offer")[0]
            notification = self._buildNotification(model)

    def notifyForOwnerAgreement(self, assignee, receivers, storeID):
        activeUsers: Dict[str, Member] = {}
        for member_model in MemberModel.objects.filter(isLoggedIn=True):
            member = self._buildMember(member_model)
            activeUsers.update({member.getUserID(): member})
        for receiver in receivers:
            if receiver in activeUsers.values():
                self.__send_channel_message(receiver.getMemberName(),
                                            "user " + str(assignee.getMemberName()) +
                                            " is nominee to be a store owner at store:  " + str(storeID))
            else:
                model = NotificationModel.objects.get_or_create(userID=assignee.getModel(),
                                                                text="user " + str(assignee.getMemberName()) +
                                                                " is nominee to be a store owner at store: " +
                                                                str(storeID))[0]
                notification = self._buildNotification(model)

    def notifyOwnerAgreementAccepted(self, receiver, storeID, oaId):
        activeUsers: Dict[str, Member] = {}
        for member_model in MemberModel.objects.filter(isLoggedIn=True):
            member = self._buildMember(member_model)
            activeUsers.update({member.getUserID(): member})
        if receiver in activeUsers.values():
            self.__send_channel_message(receiver.getMemberName(),
                                        "your agreement " + str(oaId) + " in store " + str(storeID) +
                                        " has been accepted, the nominee is wating to the" +
                                        " approvement of other store owners")
        else:
            model = NotificationModel.objects.get_or_create(userID=receiver.getModel(),
                                                            text= "your agreement " + str(oaId) + " in store " + str(storeID) +
                                                            " has been accepted, the nominee is wating to the" +
                                                            " approvement of other store owners")[0]
            notification = self._buildNotification(model)

    def notifyOwnerAgreementDeclined(self, receiver, storeID, oaID):
        activeUsers: Dict[str, Member] = {}
        for member_model in MemberModel.objects.filter(isLoggedIn=True):
            member = self._buildMember(member_model)
            activeUsers.update({member.getUserID(): member})
        if receiver in activeUsers.values():
            self.__send_channel_message(receiver.getMemberName(),
                                        "your agreement " + str(oaID) + " in store " + str(storeID) +
                                        " has been declined")
        else:
            model = \
                NotificationModel.objects.get_or_create(userID=receiver.getModel(),
                                                        text="your agreement " + str(oaID) +
                                                             " in store " + str(storeID) +
                                                             " has been declined")[0]
            notification = self._buildNotification(model)

    def _buildMember(self, model):
        return Member(model=model)

    def _buildNotification(self, model):
        return Notification(model)

    def __send_channel_message(self, group_name, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            '{}'.format(group_name),
            {
                'type': 'channel_message',
                'message': json.dumps(message)
            }
        )
