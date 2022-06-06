from typing import Dict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Backend.Business.Notifications import Notification
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
        self.__activeUsers = None  # <userId,User> should check how to initial all the activeStores into

    def notifyBoughtFromStore(self, ownersDict, storeID, buyer):
        for owner in ownersDict:
            if owner in self.__activeUsers.values():
                self.__send_channel_message(owner.getMemberName(),
                                            "user " + str(buyer.getUserID()) + "bought from store " + str(storeID))
            else:
                model = NotificationModel.objects.get_or_create(userID=buyer, text="user " + str(buyer.getUserID()) +
                                                                                   "bought from store " + str(storeID))[0]
                notification = self.__buildNotification(model)



    def _initializeDict(self):
        if self.__activeUsers is None:
            self.__activeUsers: Dict[str, User] = {}  # <userId,User> should check how to initial all the activeStores into dictionary
            for member_model in MemberModel.objects.filter(isLoggedIn=True):
                member = self._buildMember(member_model)
                self.__activeUsers.update({member.getUserID() : member})

    def __buildNotification(self, model):
        return Notification(model=model)


    def __send_channel_message(self, group_name, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            '{}'.format(group_name),
            {
                'type': 'channel_message',
                'message': message
            }
        )
