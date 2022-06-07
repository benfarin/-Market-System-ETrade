import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
django.setup()
from Backend.Business.Market import Market



class GetterManagment:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if GetterManagment.__instance is None:
            GetterManagment()
        return GetterManagment.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__market = Market.getInstance()
        if GetterManagment.__instance is None:
            GetterManagment.__instance = self

    def getProductByCategory(self, category):
        try:
            return self.__market.getProductByCategory(category)
        except Exception as e:
            raise Exception(e)

    def getProductsByName(self, nameProduct):
        try:
            return self.__market.getProductsByName(nameProduct)
        except Exception as e:
            raise Exception(e)

    def getProductByKeyWord(self, keyword):
        try:
            return self.__market.getProductByKeyWord(keyword)
        except Exception as e:
            raise Exception(e)

    def getProductPriceRange(self, minPrice, highPrice):
        try:
            return self.__market.getProductByPriceRange(minPrice, highPrice)
        except Exception as e:
            raise Exception(e)

    def getStore(self, storeId):
        try:
            return self.__market.getStore(storeId)
        except Exception as e:
            raise Exception(e)

    def getAllStores(self):
        return self.__market.getStores()


