from Business.Managment.UserManagment import UserManagment
from Business.UserPackage.User import User
from Service.Events.Events import Events
from Service.Events.EventLog import EventLog
from typing import Dict
import logging

firstAdminRegistered = False

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class UserService:

    def __init__(self):
        global firstAdminRegistered
        self.__userManagment = UserManagment.getInstance()
        self.__events = Events()
        self.systemManagerSignUp("admin", "admin", "0500000000", 999, 0, "Israel", "Be'er Sheva", "Ben-Gurion", 0,
                                 999999)
        # self.__users: Dict[str : User] = {}
        if not firstAdminRegistered:
            self.enterSystem()
            firstAdminRegistered = True

    def enterSystem(self):
        try:
            guest: User = self.__userManagment.enterSystem()
            # self.__users[guest.getUserID()] = guest
            self.__events.addEventLog(EventLog("guest login"))
            logging.info("success to enter system as a guest")
            return guest
        except Exception as e:
            logging.error("There was a problem during entering the system")
            return e

    def exitSystem(self, guestID):  # need to remove cart!
        try:
            toReturn = self.__userManagment.exitSystem(guestID)
            # self.__users.pop(guestID)
            self.__events.addEventLog(EventLog("guest logout", "guestId: ", str(guestID)))
            logging.info("success to exit system")
            return toReturn
        except Exception as e:
            logging.error("There was a problem during logout from the system")
            return e

    def memberSignUp(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum,
                     zipCode):  # address is an object of "Adress"
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            toReturn = self.__userManagment.memberSignUp(userName, password, phone, address, bank)
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
            logging.error("There was a problem during login as a member")
            return e

    def systemManagerSignUp(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum,
                            zipCode):
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            toReturn = self.__userManagment.systemManagerSignUp(userName, password, phone, address, bank)
            self.__events.addEventLog(EventLog("system managment signup", "username: " + userName,
                                               "password: " + password, "phone: " + str(phone),
                                               "bank: " + bank.printForEvents(),
                                               "address: " + address.printForEvents()))
            logging.info("success to sign new system manager " + userName)
            return toReturn
        except Exception as e:
            logging.error("Cannot signup new System Manager")
            return e

    def addProductToCart(self, userID, storeId, productId, quantity):
        try:
            self.__userManagment.addProductToCart(userID, storeId, productId, quantity)
            eventLog = EventLog("add product to cart", "userId: " + str(userID), "storeId: ", str(storeId),
                                "productId: " + str(productId), "quantity: " + str(quantity))
            logging.info("added product " + str(productId) + "to cart for user " + str(userID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            logging.error("Failed add product to cart")
            return e

    def removeProductFromCart(self, userId, storeId, productId):
        try:
            self.__userManagment.removeProductFromCart(userId, storeId, productId)
            eventLog = EventLog("remove product from cart", "userId: " + str(userId), "storeId: ", str(storeId),
                                "productId: " + str(productId))
            logging.info("removeed product " + str(productId) + " from cart for user " + userId)
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            logging.error("Failed remove product from cart")
            return e

    def updateProductFromCart(self, userID, storeID, productId, quantity):
        try:
            self.__userManagment.updateProductFromCart(userID, storeID, productId, quantity)
            eventLog = EventLog("update product from cart", "userId: " + str(userID), "storeId: ", str(storeID),
                                "productId: " + str(productId), "quantity: " + str(quantity))
            logging.info("updated product " + str(productId) + " from cart for user " + userID)
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            logging.error("Failed updating product in cart")
            return e

    def getProductByCategory(self, category):
        try:
            toReturn = self.__userManagment.getProductByCategory(category)
            self.__events.addEventLog(EventLog("get product by category", "category: " + category))
            logging.info("success to get product by category " + category)
            return toReturn
        except Exception as e:
            logging.error("Cannot find product by this category")
            return e

    def getProductByName(self, nameProduct):
        try:
            toReturn = self.__userManagment.getProductsByName(nameProduct)
            self.__events.addEventLog(EventLog("get product by name", "name: " + nameProduct))
            logging.info("success to get product by name " + nameProduct)
            return toReturn
        except Exception as e:
            logging.error("Cannot find product by this name")
            return e

    def getProductByKeyword(self, keyword):
        try:
            toReturn = self.__userManagment.getProductByKeyWord(keyword)
            self.__events.addEventLog(EventLog("get product by keyword", "keyword: " + keyword))
            logging.info("success to get product by keyword " + keyword)
            return toReturn
        except Exception as e:
            logging.error("Cannot find product by this keywords")
            return e

    def getProductPriceRange(self, minPrice, highPrice):
        try:
            toReturn = self.__userManagment.getProductPriceRange(minPrice, highPrice)
            self.__events.addEventLog(EventLog("get product by price range", "min price: " + str(minPrice),
                                               "high price: " + str(highPrice)))
            logging.info("success to get product by price range")
            return toReturn
        except Exception as e:
            logging.error("Cannot find product by this price range")
            return e

    def purchaseCart(self, userID, accountNumber, branch):
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, branch)
            self.__userManagment.purchaseCart(userID, bank)
            eventLog = EventLog("purchase cart", "userId: " + str(userID), "accountNumber: " + str(accountNumber)
                                , "branch: " + str(branch))
            logging.info("success to purchase cart for user " + str(userID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            logging.error("Failed to purchase cart for user" + str(userID))
            return e

    def getCart(self, userID):
        try:
            toReturn = self.__userManagment.getCart(userID)
            self.__events.addEventLog(EventLog("get cart", "userId: " + str(userID)))
            logging.info("success get cart for user " + str(userID))
            return toReturn
        except Exception as e:
            logging.error("Failed to get cart for user" + str(userID))
            return e
