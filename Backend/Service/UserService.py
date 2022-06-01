import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
django.setup()

from Backend.Business.Managment.UserManagment import UserManagment
from Backend.Business.Managment.GetterManagment import GetterManagment
from Backend.Business.UserPackage.Member import Member

from Backend.Business.UserPackage.User import User
from Backend.Interfaces.IMember import IMember
from Backend.Service.DTO.StoreDTO import StoreDTO
from Backend.Service.Response import Response
from Backend.Service.DTO.GuestDTO import GuestDTO
from Backend.Service.DTO.MemberDTO import MemberDTO
from Backend.Service.DTO.ProductDTO import ProductDTO
from Backend.Service.DTO.UserTransactionDTO import userTransactionDTO
from Backend.Service.DTO.CartDTO import CartDTO
from typing import Dict
import logging

from Backend.Interfaces.IStore import IStore

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class UserService:

    def __init__(self):
        self.__userManagment = UserManagment.getInstance()
        self.__getterManagment = GetterManagment.getInstance()
        # self.__users: Dict[str : User] = {}

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

    def memberLogin(self, oldUserId, userName, password):
        try:
            member = self.__userManagment.memberLogin(oldUserId, userName, password)
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
            return Response(MemberDTO(systemManager))
        except Exception as e:
            logging.error("Cannot signup new System Manager")
            return Response(e.__str__())

    def addProductToCart(self, userID, storeId, productId, quantity):
        try:
            isAdded = self.__userManagment.addProductToCart(userID, storeId, productId, quantity)
            logging.info("added product " + str(productId) + "to cart for user " + str(userID))
            return Response(isAdded)
        except Exception as e:
            logging.error("Failed add product to cart")
            return Response(e.__str__())

    def addProductToCartWithoutStore(self, userID, productID, quantity):
        try:
            isAdded = self.__userManagment.addProductToCartWithoutStore(userID, productID, quantity)
            logging.info("added product " + str(productID) + "to cart for user " + str(userID))
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
            products = self.__getterManagment.getProductByCategory(category)
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
            products = self.__getterManagment.getProductsByName(nameProduct)
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
            products = self.__getterManagment.getProductByKeyWord(keyword)
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
            products = self.__getterManagment.getProductPriceRange(minPrice, highPrice)
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

    def getSumAfterDiscount(self, userId):
        try:
            totalAmount = self.__userManagment.getSumAfterDiscount(userId)
            logging.info("success get sum after discount " + str(userId))
            return Response(totalAmount)
        except Exception as e:
            logging.error("Failed to get sum after discount" + str(userId))
            return Response(e.__str__())

    def getUserByUserName(self, username):
        try:
            user = self.__userManagment.getUserByUserName(username)
            logging.info("success get user " + str(username))
            if isinstance(user, Member):
                return Response(MemberDTO(user))
            return Response(GuestDTO(user))
        except Exception as e:
            logging.error("Failed to get user" + str(username))
            return Response(e.__str__())





