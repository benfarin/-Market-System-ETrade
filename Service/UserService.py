from Business.Managment.UserManagment import UserManagment
from Service.Events.Events import Events
from Service.Events.EventLog import EventLog


class UserService:
    def __init__(self):
        self.__userManagment = UserManagment()
        self.__events = Events()

    def guestLogin(self):
        try:
            toReturn = self.__userManagment.guestLogin()
            self.__events.addEventLog(EventLog("guest login"))
            return toReturn
        except Exception as e:
            return e

    def guestLogOut(self, guestID):  # need to remove cart!
        try:
            toReturn = self.__userManagment.guestLogOut(guestID)
            self.__events.addEventLog(EventLog("guest logout", "guestId: ", str(guestID)))
            return toReturn
        except Exception as e:
            return e

    def memberSignUp(self, userName, password, phone,  accountNumber, brunch, country, city, street, apartmentNum, zipCode, icart):  # address is an object of "Adress"
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            toReturn = self.__userManagment.memberSignUp(userName, password, phone, address, bank, icart)
            self.__events.addEventLog(EventLog("member sign up", "user name: " + userName, "password: " + password,
                                               "phone: " + phone, "address: " + address.printForEvents(),
                                               "bank: " + bank.printForEvents()))
            return toReturn
        except Exception as e:
            return e

    def memberLogin(self, userID, password):
        try:
            toReturn = self.__userManagment.memberLogin(userID, password)
            self.__events.addEventLog(EventLog("member login", "userId: " + str(userID), "password: " + password))
            return toReturn
        except Exception as e:
            return e

    def logoutMember(self, userID):
        try:
            toReturn = self.__userManagment.logoutMember(userID)
            self.__events.addEventLog(EventLog("member logout", "userId: " + str(userID)))
            return toReturn
        except Exception as e:
            return e

    def systemManagerSignUp(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum, zipCode):
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            toReturn = self.__userManagment.systemManagerSignUp(userName, password, phone, address, bank)
            self.__events.addEventLog(EventLog("system managment signup", "username: " + userName,
                                               "password: " + password, "phone: " + str(phone),
                                               "bank: " + bank.printForEvents(), "address: " + address.printForEvents()))
            return toReturn
        except Exception as e:
            return e