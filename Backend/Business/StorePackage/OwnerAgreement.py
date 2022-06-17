from typing import Dict

from Backend.Business.Notifications.NotificationHandler import NotificationHandler
from Backend.Business.UserPackage.Member import Member
from Backend.Interfaces.IMember import IMember
from ModelsBackend.models import OwnerAgreementModel


class OwnerAgreement:

    def __init__(self, assigner=None, assignee=None, storeId=None, receivers=None, model=None):
        if model is None:
            self.__model = OwnerAgreementModel.objects.get_or_create(assigner=assigner.getModel(),
                                                                     assignee=assignee.getModel(),
                                                                     storeID=storeId.getModel())[0]
            for receiver in receivers:
                self.__model.permissionsOwners.add(receiver.getModel())
            self.__OA_ID = self.__model.id
            self.__assigner = assigner
            self.__assignee = assignee
            self.__storeID = storeId.getStoreId()
            self.__active = True
            self.__isAccepted = False
            self.__receivers: Dict[IMember: bool] = {}
            for receiver in receivers:
                self.__receivers[receiver] = False
            self.__receivers[assigner] = True
            if len(self.__receivers) == 1:
                self.__isAccepted = True
        else:
            self.__OA_ID = self.__model.id
            self.__assigner = self._buildMember(self.__model.assigner)
            self.__assignee = self._buildMember(self.__model.assignee)
            self.__storeID = self.__model.storeID.storeID
            self.__active = self.__model.active
            self.__isAccepted = self.__model.isAccepted
            receivers_model = self.__model.permissionsOwners.through.objects.all()
            for receiver_model in receivers_model:
                receiver = self._buildMember(receiver_model)
                self.__receivers[receiver] = False
            self.__receivers[self._buildMember(self.__assigner)] = True
            if len(self.__receivers) == 1:
                self.__isAccepted = True

    def getOwnerAgreementId(self):
        return self.__OA_ID

    def getAssigner(self):
        return self.__assigner

    def getAssignee(self):
        return self.__assignee

    def get_storeID(self):
        return self.__storeID

    def get_Accepted(self):
        return self.__isAccepted

    def acceptOffer(self, userID):
        self.__receivers[userID] = True
        check = self.__receivers.values()
        if all(check):
            notification_handler: NotificationHandler = NotificationHandler.getInstance()
            notification_handler.notifyOwnerAgreementAccepted(self.__assignee, self.__storeID, self.__OA_ID)
            self.__model.isAccepted = True
            self.__model.save()
            self.__isAccepted = True
            return True
        return False

    def rejectOffer(self):
        self.__active = False
        self.__model.active = False
        self.__model.save()
        notification_handler: NotificationHandler = NotificationHandler.getInstance()
        notification_handler.notifyOwnerAgreementDeclined(self.__assignee, self.__storeID, self.__OA_ID)
        self.__model.delete()

    def _buildMember(self, model):
        return Member(model=model)

    def removeOwnerAgreement(self):
        self.__model.delete()
