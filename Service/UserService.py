from Business.Managment.UserManagment import UserManagment
from interfaces import IUser


class UserService:
    def __init__(self):
        self.__userManagment: IUser = UserManagment()

    def guestLogin(self):
        return self.__userManagment.guestLogin()

    def guestLogOut(self, guestID):  # need to remove cart!
        return self.__userManagment.guestLogOut(guestID)

    def memberSignUp(self, userName, password, phone, address, bank, icart):  # address is an object of "Adress"
        return self.__userManagment.memberSignUp(userName, password, phone, address, bank, icart)

    def memberLogin(self, userID, password):
        return self.__userManagment.memberLogin(userID, password)

    def logoutMember(self, userID):
        return self.__userManagment.logoutMember(userID)

    def checkPassword(self, userID, password):
        return self.__userManagment.checkPassword(userID, password)

    def checkOnlineUser(self, userID):
        return self.__userManagment.checkOnlineUser(userID)

    def checkAssigners(self, assignerID, assigneID):
        return self.__userManagmentcheckAssigners(assignerID, assigneID)

    def saveProducts(self, userID, store):
        return self.__userManagment.saveProducts(userID, store)

    def appointManagerToStore(self, storeID, assignerID, assigneID):  # check if the asssigne he member and assignerID!!
        return self.__userManagment.appointManagerToStore(storeID, assignerID, assigneID)

    def appointOwnerToStore(self, storeID, assignerID, assigneID):  # check if the asssigne he member and assignerID!!
        return self.__userManagment.appointOwnerToStore(storeID, assignerID, assigneID)

    def setStockManagementPermission(self, storeID, assignerID, assigneID):
        return self.__userManagment.setStockManagementPermission(storeID, assignerID, assigneID)

    def setAppointManagerPermission(self, storeID, assignerID, assigneID):
        return self.__userManagment.setAppointManagerPermission(storeID, assignerID, assigneID)

    def setAppointOwnerPermission(self, storeID, assignerID, assigneID):
        return self.__userManagment.setAppointOwnerPermission(self, storeID, assignerID, assigneID)

    def setChangePermission(self, storeID, assignerID, assigneID):
        return self.__userManagment.setChangePermission(storeID, assignerID, assigneID)

    def setRolesInformationPermission(self, storeID, assignerID, assigneID):
        return self.__userManagment.setRolesInformationPermission(storeID, assignerID, assigneID)

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneID):
        return self.__userManagment.setPurchaseHistoryInformationPermission(storeID, assignerID, assigneID)
