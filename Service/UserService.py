from Business.Managment.UserManagment import UserManagment
from Business.UserPackage.User import User
from Service.DTO.StoreTransactionForUserDTO import storeTransactionForUserDTO
from Service.DTO.BagDTO import BagDTO
from Service.DTO.ProductDTO import ProductDTO
from Service.Response import Response
from Service.DTO.GuestDTO import guestDTO
from Service.DTO.MemberDTO import memberDTO
from Service.DTO.BankDTO import bankDTO
from Service.DTO.AddressDTO import adressDTO
from Service.DTO.CartDTO import cartDTO
from Service.DTO.userTransactionDTO import userTransactionDTO
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
            logging.info("success to enter system as a guest")
            return Response(guestDTO(guest.getUserID(), self.__makeCartDTO(guest.getUserID(), guest.getCart())))
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
            member = self.__userManagment.memberSignUp(userName, password, phone, address, bank)
            logging.info("success to register user " + userName)

            dtoBAnk = bankDTO(accountNumber, brunch)
            dtoAddress = adressDTO(country, city, street, apartmentNum, zipCode)
            dtoCart = self.__makeCartDTO(member.getUserID(), member.getCart())
            dtoTransactions = self.__makeDtoTransaction(member.getUserID(), member.getTransactions())

            return Response(memberDTO(member.getUserID(), member.getMemberName(), member.getPhone(),
                                      dtoAddress, dtoBAnk, dtoTransactions, member.getPaymentsIds(), dtoCart))
        except Exception as e:
            logging.warning("There was a problem during registration process")
            return Response(e.__str__())

    def memberLogin(self, userName, password):
        try:
            isLoggedIn = self.__userManagment.memberLogin(userName, password)
            logging.info("success to login user " + userName)
            return Response(isLoggedIn)
        except Exception as e:
            logging.error("There was a problem during login as a member")
            return Response(e.__str__())

    def systemManagerSignUp(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum,
                            zipCode):
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, brunch)
            address = self.__userManagment.createAddress(country, city, street, apartmentNum, zipCode)
            toReturn = self.__userManagment.systemManagerSignUp(userName, password, phone, address, bank)
            logging.info("success to sign new system manager " + userName)
            return toReturn
        except Exception as e:
            logging.error("Cannot signup new System Manager")
            return e

    def addProductToCart(self, userID, storeId, productId, quantity):
        try:
            self.__userManagment.addProductToCart(userID, storeId, productId, quantity)
            logging.info("added product " + str(productId) + "to cart for user " + str(userID))
            return True
        except Exception as e:
            logging.error("Failed add product to cart")
            return e

    def removeProductFromCart(self, userId, storeId, productId):
        try:
            self.__userManagment.removeProductFromCart(userId, storeId, productId)
            logging.info("removeed product " + str(productId) + " from cart for user " + userId)
            return True
        except Exception as e:
            logging.error("Failed remove product from cart")
            return e

    def updateProductFromCart(self, userID, storeID, productId, quantity):
        try:
            self.__userManagment.updateProductFromCart(userID, storeID, productId, quantity)
            logging.info("updated product " + str(productId) + " from cart for user " + userID)
            return True
        except Exception as e:
            logging.error("Failed updating product in cart")
            return e

    def getProductByCategory(self, category):
        try:
            toReturn = self.__userManagment.getProductByCategory(category)
            logging.info("success to get product by category " + category)
            return toReturn
        except Exception as e:
            logging.error("Cannot find product by this category")
            return e

    def getProductByName(self, nameProduct):
        try:
            toReturn = self.__userManagment.getProductsByName(nameProduct)
            logging.info("success to get product by name " + nameProduct)
            return toReturn
        except Exception as e:
            logging.error("Cannot find product by this name")
            return e

    def getProductByKeyword(self, keyword):
        try:
            toReturn = self.__userManagment.getProductByKeyWord(keyword)
            logging.info("success to get product by keyword " + keyword)
            return toReturn
        except Exception as e:
            logging.error("Cannot find product by this keywords")
            return e

    def getProductPriceRange(self, minPrice, highPrice):
        try:
            toReturn = self.__userManagment.getProductPriceRange(minPrice, highPrice)
            logging.info("success to get product by price range")
            return toReturn
        except Exception as e:
            logging.error("Cannot find product by this price range")
            return e

    def purchaseCart(self, userID, accountNumber, branch):
        try:
            bank = self.__userManagment.createBankAcount(accountNumber, branch)
            self.__userManagment.purchaseCart(userID, bank)
            logging.info("success to purchase cart for user " + str(userID))
            return True
        except Exception as e:
            logging.error("Failed to purchase cart for user" + str(userID))
            return e

    def getCart(self, userID):
        try:
            toReturn = self.__userManagment.getCart(userID)
            logging.info("success get cart for user " + str(userID))
            return toReturn
        except Exception as e:
            logging.error("Failed to get cart for user" + str(userID))
            return e

    def __makeDtoTransaction(self, userId, userTransactions):
        transactionList = []
        for ut in userTransactions:
            transactionId = ut.getUserTransactionId()
            paymentId = ut.getPaymentId()

            storeTransactions = ut.getStoreTransactions()
            storeTransactionsDtoList = []
            for st in storeTransactions.keys():
                storeName = st.getStoreName()
                amount = st.getAmount()
                products = st.getProducts()

                productDTOList = []
                for product in products:
                    productId = product.getProductId()
                    productName = product.getProductName()
                    productPrice = product.getProductPrice()
                    productCategory = product.getProductCategory()
                    productKeywords = product.getProductKeywords()

                    dtoProduct = ProductDTO(productId, productName, productPrice, productCategory, productKeywords)
                    productDTOList.append(dtoProduct)

                storeTransactionsDtoList.append(storeTransactionForUserDTO(storeName, productDTOList, amount))

            transactionList.append(userTransactionDTO(userId, transactionId, storeTransactionsDtoList, paymentId))

        return transactionList

    def __makeCartDTO(self, userId, cart):
        bagList: Dict[int: BagDTO] = {}
        for bag in cart.getAllBags():
            products: Dict[int: ProductDTO] = {}
            for product in bag.getProducts():
                dtoProduct = ProductDTO(product.getProductId(), product.getProductName(), product.getProductPrice(),
                                        product.getProductCategory(), product.getProductKeywords())
                products[product.getProductId()] = dtoProduct

            bagList[bag.getStoreId()] = BagDTO(userId, products)
        return cartDTO(userId, bagList)
