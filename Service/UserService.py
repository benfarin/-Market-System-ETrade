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