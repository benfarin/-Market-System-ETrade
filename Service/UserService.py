from Business.UserManagment import UserManagment
from interfaces import IUser
class UserService:
    def __init__(self):
        self.__userManagment : IUser = UserManagment()
    def guestLogin(self):
        return self.__userManagment.guestLogin()

    def guestLogOut(self, guestID): #need to remove cart!
        return self.__userManagment. guestLogOut( guestID)

    def memberSignUp(self,userName, password, phone, address, bank , icart): #address is an object of "Adress"
        return self.__userManagment. memberSignUp(userName, password, phone, address, bank , icart)


    def memberLogin(self,userName, password):
        return self.__userManagment.memberLogin(userName, password)

    def logoutMember(self,userName):
        return self.__userManagment.logoutMember(userName)
    def checkPassword(self,userName ,password):
        return self.__userManagment.checkPassword(userName ,password)
    def checkOnlineUser(self,userName):
        return self.__userManagment.checkOnlineUser(userName)

    def checkAssigners(self, assignerName, assigneName):
        return self.__userManagmentcheckAssigners( assignerName, assigneName)

    def saveProducts(self,userName,store):
        return self.__userManagment.saveProducts(userName,store)

    def appointManagerToStore(self,storeID, assignerName , assigneName ): # check if the asssigne he member and assignerID!!
        return self.__userManagment.appointManagerToStore(storeID, assignerName , assigneName)
    def appointOwnerToStore(self,storeID, assignerName , assigneName):# check if the asssigne he member and assignerID!!
        return self.__userManagment.appointOwnerToStore(storeID, assignerName , assigneName)

    def setStockManagementPermission(self,storeID, assignerName, assigneName):
        return self.__userManagment.setStockManagementPermission(storeID, assignerName, assigneName)

    def setAppointManagerPermission(self,storeID ,assignerName, assigneName):
        return self.__userManagment.setAppointManagerPermission(storeID ,assignerName, assigneName)

    def setAppointOwnerPermission(self,storeID ,assignerName, assigneName):
        return self.__userManagment.setAppointOwnerPermission(self,storeID ,assignerName, assigneName)

    def setChangePermission(self,storeID ,assignerName, assigneName):
        return self.__userManagment.setChangePermission(storeID ,assignerName, assigneName)

    def setRolesInformationPermission(self,storeID, assignerName, assigneName):
        return  self.__userManagment.setRolesInformationPermission(storeID, assignerName, assigneName)

    def setPurchaseHistoryInformationPermission(self,storeID, assignerName, assigneName):
        return self.__userManagment.setPurchaseHistoryInformationPermission(storeID, assignerName, assigneName)
