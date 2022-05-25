from Backend.Business.Managment.MemberManagment import MemberManagment
from Backend.Business.Managment.RoleManagment import RoleManagment
from Backend.Service.Response import Response
from Backend.Service.DTO.StoreDTO import StoreDTO
from Backend.Service.DTO.UserTransactionDTO import userTransactionDTO
from Backend.Service.DTO.StoreTransactionForUserDTO import storeTransactionForUserDTO
from Backend.Service.DTO.ProductDTO import ProductDTO
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MemberService:

    def __init__(self):
        self.__memberManage = MemberManagment.getInstance()
        self.__roleManagment = RoleManagment.getInstance()

    def createStore(self, storeName, founderId, accountNumber, brunch, country, city, street, apartmentNum, zipCode):
        try:
            bank = self.__memberManage.createBankAcount(accountNumber, brunch)
            address = self.__memberManage.createAddress(country, city, street, apartmentNum, zipCode)
            store = self.__memberManage.createStore(storeName, founderId, bank, address)

            logging.info("succeeded create store " + storeName)
            return Response(StoreDTO(store))

        except Exception as e:
            logging.error("Failed opening a new store")
            return Response(e.__str__())

    def removeStore(self, storeId, userId):
        try:
            isRemoved = self.__memberManage.removeStore(userId, storeId)
            logging.info("remove store: " + userId)
            return Response(isRemoved)
        except Exception as e:
            logging.error("Failed remove the store: " + str(storeId))
            return Response(e.__str__())

    def recreateStore(self, founderId, storeId):
        try:
            isRemoved = self.__memberManage.recreateStore(founderId, storeId)
            logging.info("recreate store: " + founderId)
            return Response(isRemoved)
        except Exception as e:
            logging.error("Failed recreate the store: " + str(storeId))
            return Response(e.__str__())

    def logoutMember(self, userName):
        try:
            isLoggedOut = self.__memberManage.logoutMember(userName)
            logging.info("logout member: " + userName)
            return Response(isLoggedOut)
        except Exception as e:
            logging.error("Failed to logged out")
            return Response(e.__str__())

    def getMemberTransactions(self, userID):
        try:
            transactions = self.__memberManage.getMemberTransactions(userID)
            logging.info("")
            transaction_DTO = []
            for transaction in transactions:
                transaction_DTO.append(userTransactionDTO(transaction))
            return Response(transaction_DTO)
        except Exception as e:
            logging.error("Failed opening a new store")
            return Response(e.__str__())

    def isSystemManger(self, userName):
        try:
            isSM = self.__memberManage.isSystemManger(userName)
            logging.info("success to get is system manager:  " + str(userName))
            return Response(isSM)
        except Exception as e:
            logging.error("Failed to get system manager! ")
            return Response(e.__str__())



