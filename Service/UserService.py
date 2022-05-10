from Business.Managment.UserManagment import UserManagment
from Business.UserPackage.User import User
from Service.DTO.StoreDTO import StoreDTO
from Service.Response import Response
from Service.DTO.GuestDTO import GuestDTO
from Service.DTO.MemberDTO import MemberDTO
from Service.DTO.ProductDTO import ProductDTO
from Service.DTO.userTransactionDTO import userTransactionDTO
from Service.DTO.CartDTO import CartDTO
from typing import Dict
import logging

from interfaces.IStore import IStore

firstAdminRegistered = False

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class UserService:

    def __init__(self):
        global firstAdminRegistered
        self.__userManagment = UserManagment.getInstance()
        self.systemManagerSignUp("admin", "admin", "0500000000", 999, 0, "Israel", "Be'er Sheva", "Ben-Gurion", 0,
                                 999999)
        # self.__users: Dict[str : User] = {}
        if not firstAdminRegistered:
            self.enterSystem()
            firstAdminRegistered = True

    def enterSystem(self):
        try:
            guest = self.__userManagment.enterSystem()
            # self.__users[guest.getUserID()] = guest
            logging.info("success to enter system as a guest")
            return Response(GuestDTO(guest))
        except Exception as e:
            logging.error("There was a problem during entering the system")
            return Response(e.__str__())

    def exitSystem(self, guestID):  # need to remove cart!
        try:
            isExit = self.__userManagment.exitSystem(guestID)
            # self.__users.pop(guestID)
            logging.info("success to exit system")
            return Response(isExit)
        except Exception as e:
            logging.error("There was a problem during logout from the system")
            return Response(e.__str__())

    def memberSignUp(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum,
                     zipCode):  # address is an object of "Adress"
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            isSignuped = self.__userManagment.memberSignUp(userName, password, phone, address, bank)
            logging.info("success to register user " + userName)

            return Response(isSignuped)
        except Exception as e:
            logging.warning("There was a problem during registration process")
            return Response(e.__str__())

    def memberLogin(self, userName, password):
        try:
            member = self.__userManagment.memberLogin(userName, password)
            logging.info("success to login user " + userName)
            return Response(MemberDTO(member))
        except Exception as e:
            logging.error("There was a problem during login as a member")
            return Response(e.__str__())

    def systemManagerSignUp(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum,
                            zipCode):
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            systemManager = self.__userManagment.systemManagerSignUp(userName, password, phone, address, bank)
            logging.info("success to sign new system manager " + userName)
            return MemberDTO(systemManager)
        except Exception as e:
            logging.error("Cannot signup new System Manager")
            return e

    def addProductToCart(self, userID, storeId, productId, quantity):
        try:
            isAdded = self.__userManagment.addProductToCart(userID, storeId, productId, quantity)
            logging.info("added product " + str(productId) + "to cart for user " + str(userID))
            return Response(isAdded)
        except Exception as e:
            logging.error("Failed add product to cart")
            return Response(e.__str__())

    def removeProductFromCart(self, userId, storeId, productId):
        try:
            isRemoved = self.__userManagment.removeProductFromCart(userId, storeId, productId)
            logging.info("removeed product " + str(productId) + " from cart for user " + userId)
            return Response(isRemoved)
        except Exception as e:
            logging.error("Failed remove product from cart")
            return Response(e.__str__())

    def updateProductFromCart(self, userID, storeID, productId, quantity):
        try:
            isUpdated = self.__userManagment.updateProductFromCart(userID, storeID, productId, quantity)
            logging.info("updated product " + str(productId) + " from cart for user " + userID)
            return Response(isUpdated)
        except Exception as e:
            logging.error("Failed updating product in cart")
            return Response(e.__str__())

    def getProductByCategory(self, category):
        try:
            products = self.__userManagment.getProductByCategory(category)
            logging.info("success to get product by category " + category)

            productsDTOs = []
            for product in products:
                productsDTOs.append(ProductDTO(product))
            return Response(productsDTOs)
        except Exception as e:
            logging.error("Cannot find product by this category")
            return Response(e.__str__())

    def getProductByName(self, nameProduct):
        try:
            products = self.__userManagment.getProductsByName(nameProduct)
            logging.info("success to get product by name " + nameProduct)

            productsDTOs = []
            for product in products:
                productsDTOs.append(ProductDTO(product))
            return Response(productsDTOs)
        except Exception as e:
            logging.error("Cannot find product by this name")
            return Response(e.__str__())

    def getProductByKeyword(self, keyword):
        try:
            products = self.__userManagment.getProductByKeyWord(keyword)
            logging.info("success to get product by keyword " + keyword)

            productsDTOs = []
            for product in products:
                productsDTOs.append(ProductDTO(product))
            return Response(productsDTOs)
        except Exception as e:
            logging.error("Cannot find product by this keywords")
            return Response(e.__str__())

    def getProductPriceRange(self, minPrice, highPrice):
        try:
            products = self.__userManagment.getProductPriceRange(minPrice, highPrice)
            logging.info("success to get product by price range")

            productsDTOs = []
            for product in products:
                productsDTOs.append(ProductDTO(product))
            return Response(productsDTOs)
        except Exception as e:
            logging.error("Cannot find product by this price range")
            return Response(e.__str__())

    def purchaseCart(self, userID, accountNumber, branch):
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, branch)
            userTransaction = self.__userManagment.purchaseCart(userID, bank)
            logging.info("success to purchase cart for user " + str(userID))
            return Response(userTransactionDTO(userTransaction))
        except Exception as e:
            logging.error("Failed to purchase cart for user" + str(userID))
            return Response(e.__str__())

    def getCart(self, userID):
        try:
            cart = self.__userManagment.getCart(userID)
            logging.info("success get cart for user " + str(userID))
            return Response(CartDTO(cart))
        except Exception as e:
            logging.error("Failed to get cart for user" + str(userID))
            return Response(e.__str__())

    def getStore(self, storeID):
        try:
            store = self.__userManagment.getStore(storeID)
            logging.info("success get store " + str(storeID))
            return Response(StoreDTO(store))
        except Exception as e:
            logging.error("Failed to get store " + str(storeID))
            return Response(e.__str__())

    def getAllStores(self):
        try:
            stores: Dict[int, IStore] = self.__userManagment.getAllStores()
            logging.info("success get stores in market")

            storesDTOs = []
            for store in stores.values():
                storesDTOs.append(StoreDTO(store))
            return Response(storesDTOs)
        except Exception as e:
            logging.error("Failed to get stores")
            return Response(e.__str__())


    def getAllStoresOfUser(self, userId):
        try:
            stores = self.__userManagment.getAllStoresOfUser(userId)
            logging.info("success get stores in market")

            storesDTOs = []
            for store in stores:
                storesDTOs.append(StoreDTO(store))
            return Response(storesDTOs)
        except Exception as e:
            logging.error("Failed to get stores")
            return Response(e.__str__())


    def getUserIdByName(self, user_name):
        try:
            name = self.__userManagment.getUserIdByName(user_name)
            logging.info("success get user id")
            return Response(name)
        except Exception as e:
            logging.error("Failed to get user id")
            return Response(e.__str__())

