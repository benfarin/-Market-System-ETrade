from Business.Managment.UserManagment import UserManagment
from Service.Events.Events import Events
from Service.Events.EventLog import EventLog
import logging


class UserService:
    def __init__(self):
        self.__userManagment = UserManagment()
        self.__events = Events()

    def guestLogin(self):
        try:
            toReturn = self.__userManagment.guestLogin()
            self.__events.addEventLog(EventLog("guest login"))
            logging.info("success to enter system as a guest")
            return toReturn
        except Exception as e:
            logging.error("There was a problem during entering the system")
            return e

    def guestLogOut(self, guestID):  # need to remove cart!
        try:
            toReturn = self.__userManagment.guestLogOut(guestID)
            self.__events.addEventLog(EventLog("guest logout", "guestId: ", str(guestID)))
            logging.info("success to exit system")
            return toReturn
        except Exception as e:
            logging.error("There was a problem during logout from the system")
            return e

    def memberSignUp(self, userName, password, phone,  accountNumber, brunch, country, city, street, apartmentNum, zipCode, icart):  # address is an object of "Adress"
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            toReturn = self.__userManagment.memberSignUp(userName, password, phone, address, bank, icart)
            self.__events.addEventLog(EventLog("member sign up", "user name: " + userName, "password: " + password,
                                               "phone: " + phone, "address: " + address.printForEvents(),
                                               "bank: " + bank.printForEvents()))
            logging.info("success to register user " + userName)
            return toReturn
        except Exception as e:
            logging.warning("There was a problem during registration process")
            return e

    def memberLogin(self, userName, password):
        try:
            toReturn = self.__userManagment.memberLogin(userName, password)
            self.__events.addEventLog(EventLog("member login", "username: " + userName, "password: " + password))
            logging.info("success to login user " + userName)
            return toReturn
        except Exception as e:
            logging.error("There was a problem during login, try again")
            return e

    def logoutMember(self, userName):
        try:
            self.__userManagment.logoutMember(userName)
            self.__events.addEventLog(EventLog("member logout", "userId: " + userName))
            logging.info("success to logout user " + userName)
            return True
        except Exception as e:
            logging.error("There was a problem to logout from the market")
            return e

    def systemManagerSignUp(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum, zipCode):
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            toReturn = self.__userManagment.systemManagerSignUp(userName, password, phone, address, bank)
            self.__events.addEventLog(EventLog("system managment signup", "username: " + userName,
                                               "password: " + password, "phone: " + str(phone),
                                               "bank: " + bank.printForEvents(), "address: " + address.printForEvents()))
            logging.info("success to sign new system manager " + userName)
            return toReturn
        except Exception as e:
            logging.error("Cannot signup new System Manager")
            return e