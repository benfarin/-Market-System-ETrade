class adressDTO():
    def __init__(self, country, city, street, apartmentNum, zipCode):
        self.__country = country
        self.__city = city
        self.__street = street
        self.__apartmentNum = apartmentNum
        self.__zipCode = zipCode

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
