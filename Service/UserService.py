from Business.Managment.UserManagment import UserManagment
from Service.Events.Events import Events
from Service.Events.EventLog import EventLog


class UserService:
    def __init__(self):
        self.__userManagment = UserManagment()
        self.__events = Events()

    def guestLogin(self):
        try:
            self.__userManagment.guestLogin()
            self.__events.addEventLog(EventLog("guest login"))
            return True
        except Exception as e:
            return e

    def guestLogOut(self, guestID):  # need to remove cart!
        try:
            self.__userManagment.guestLogOut(guestID)
            self.__events.addEventLog(EventLog("guest logout", "guestId: ", str(guestID)))
            return True
        except Exception as e:
            return e

    def memberSignUp(self, userName, password, phone,  accountNumber, brunch, country, city, street, apartmentNum, zipCode, icart):  # address is an object of "Adress"
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            self.__userManagment.memberSignUp(userName, password, phone, address, bank, icart)
            self.__events.addEventLog(EventLog("member sign up", "user name: " + userName, "password: " + password,
                                               "phone: " + phone, "address: " + address.printForEvents(),
                                               "bank: " + bank.printForEvents()))
            return True
        except Exception as e:
            return e

    def memberLogin(self, userID, password):
        try:
            self.__userManagment.memberLogin(userID, password)
            self.__events.addEventLog(EventLog("member login", "userId: " + str(userID), "password: " + password))
            return True
        except Exception as e:
            return e

    def logoutMember(self, userID):
        try:
            self.__userManagment.logoutMember(userID)
            self.__events.addEventLog(EventLog("member logout", "userId: " + str(userID)))
            return True
        except Exception as e:
            return e
