from Business.Managment.MemberManagment import MemberManagment
from Business.Managment.RoleManagment import RoleManagment
from Service.Events.Events import Events
from Service.Events.EventLog import EventLog
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MemberService:

    def __init__(self):
        self.__memberManage = MemberManagment.getInstance()
        self.__roleManagment = RoleManagment.getInstance()
        self.__events = Events()

    def getEvents(self):
        return self.__events

    def createStore(self, storeName, founderId, accountNumber, brunch, country, city, street, apartmentNum, zipCode):
        try:
            bank = self.__memberManage.createBankAcount(accountNumber, brunch)
            address = self.__memberManage.createAddress(country, city, street, apartmentNum, zipCode)
            toReturn = self.__memberManage.createStore(storeName, founderId, bank, address)
            eventLog = EventLog("create store", "store name: " + storeName, "founderId: " + founderId,
                                "bankAccount: " + bank.printForEvents(), "address: " + address.printForEvents())
            logging.info("create store", "store name: " + storeName, "founderId: " + founderId,
                         "bankAccount: " + bank.printForEvents(), "address: " + address.printForEvents())
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            logging.error("Failed opening a new store")
            return e

    def logoutMember(self, userName):
        try:
            toReturn = self.__memberManage.logoutMember(userName)
            eventLog = EventLog("")
            logging.info("")
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            logging.error("Failed opening a new store")
            return e

    def getMemberTransactions(self, userID):
        try:
            toReturn = self.__memberManage.getMemberTransactions(userID)
            eventLog = EventLog("")
            logging.info("")
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            logging.error("Failed opening a new store")
            return e
