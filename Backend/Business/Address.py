
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()

from ModelsBackend.models import AddressModel

class Address:

    def __init__(self, country=None, city=None, street=None, apartmentNum=None, zipCode=None, model=None):
        # self.__country = country
        # self.__city = city
        # self.__street = street
        # self.__apartmentNum = apartmentNum
        # self.__zipCode = zipCode
        if model is None:
            self.__model = AddressModel.objects.get_or_create(country=country, city=city, street=street,
                                                              apartmentNum=apartmentNum, zipCode=zipCode)[0]
        else:
            self.__model = model

    def getCountry(self):
        return self.__model.country

    def setCountry(self, country):
        self.__model.country = country
        self.__model.save()

    def getCity(self):
        return self.__model.city

    def setCity(self, city):
        self.__model.city = city
        self.__model.save()

    def getStreet(self):
        return self.__model.street

    def setStreet(self, street):
        self.__model.street = street
        self.__model.save()

    def getApartmentNum(self):
        return self.__model.apartmentNum

    def setApartmentNum(self, apartmentNum):
        self.__model.apartmentNum = apartmentNum
        self.__model.save()

    def getZipCode(self):
        return self.__model.zipCode

    def setZipCode(self, zipCode):
        self.__model.zipCode = zipCode
        self.__model.save()

    def getModel(self):
        return self.__model

    def printForEvents(self):
        address = "\n\t\t\tcountry: " +self.__model.country
        address += "\n\t\t\tcity: " + self.__model.city
        address += "\n\t\t\tstreet: " + self.__model.street
        address += "\n\t\t\tapartment number: " + str(self.__model.apartmentNum)
        return address + "\n\t\t\tzip code: " + str(self.__model.zipCode)

    def removeAddress(self):
        self.__model.delete()

    def __eq__(self, other):
        return isinstance(other, Address) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__model.country and self.__model.country and self.__model.city and
                    self.__model.street and self.__model.apartmentNum and self.__model.zipCode)


    # def __str__(self):
    #     return "Country: " + self.__country + " city: " + self.__city + " street: " + self.__street + " apartment Number: " \
    #            + self.__apartmentNum + " zip code: " + self.__zipCode