from Business.Address import Address


class AddressDTO:
    def __init__(self, address: Address):
        self.__country = address.getCountry()
        self.__city = address.getCity()
        self.__street = address.getStreet()
        self.__apartmentNum = address.getApartmentNum()
        self.__zipCode = address.getZipCode()

    def getCountry(self):
        return self.__country

    def setCountry(self, country):
        self.__country = country

    def getCity(self):
        return self.__city

    def setCity(self, city):
        self.__city = city

    def getStreet(self):
        return self.__street

    def setStreet(self, street):
        self.__street = street

    def getApartmentNum(self):
        return self.__apartmentNum
