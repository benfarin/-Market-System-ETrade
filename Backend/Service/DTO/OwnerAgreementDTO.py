from Backend.Business.StorePackage.OwnerAgreement import OwnerAgreement
from Backend.Service.DTO.MemberDTO import MemberDTO


class OwnerAgreementDTO:

    def __init__(self, ownerAgreement: OwnerAgreement):
        self.__oaId = ownerAgreement.getOwnerAgreementId()
        self.__assigner = MemberDTO(ownerAgreement.getAssigner())
        self.__assignee = MemberDTO(ownerAgreement.getAssignee())
        self.__storeId = ownerAgreement.get_storeID()
        self.__isAccepted = ownerAgreement.get_Accepted()

    def getOwnerAgreementId(self):
        return self.__oaId

    def getAssigner(self):
        return self.__assigner

    def getAssignee(self):
        return self.__assignee

    def getStoreId(self):
        return self.__storeId

    def getIsAccepted(self):
        return self.__isAccepted

    def __str__(self):
        toReturn = "Owner Agreement " + str(self.__oaId)
        toReturn += "\n\tassigner: " + self.__assigner.__str__()
        toReturn += "\n\tassignee: " + self.__assignee.__str__()
        toReturn += "\n\tstore Id: " + str(self.__storeId)
        return toReturn + "\n\tis accepted: " + str(self.__isAccepted)

