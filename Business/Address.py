class Address:

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

    def setApartmentNum(self, apartmentNum):
        self.__apartmentNum = apartmentNum

    def getZipCode(self):
        return self.__zipCode

    def setZipCode(self, zipCode):
        self.__zipCode = zipCode

    def printForEvents(self):
        address = "\n\t\t\tcountry: " + self.__country
        address += "\n\t\t\tcity: " + self.__city
        address += "\n\t\t\tstreet: " + self.__street
        address += "\n\t\t\tapartment number: " + str(self.__apartmentNum)
        return address + "\n\t\t\tzip code: " + str(self.__zipCode)

    # def __str__(self):
    #     return "Country: " + self.__country + " city: " + self.__city + " street: " + self.__street + " apartment Number: " \
    #            + self.__apartmentNum + " zip code: " + self.__zipCode