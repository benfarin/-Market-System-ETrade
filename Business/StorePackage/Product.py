class Product:

    def __init__(self, Id, name, price, category):
        self.__id = Id
        self.__name = name
        self.__price = price
        self.__category = category  # String
        self.__rating = 0
        self.__numOfRatings = 0

    def getProductId(self):
        return self.__id

    def getProductName(self):
        return self.__name

    def getProductPrice(self):
        return self.__price

    def setProductPrice(self, price):
        self.__price = price

    def getProductCategory(self):
        return self.__category

    def getProductRating(self):
        return self.__rating

    def setProductRating(self, rating):
        if rating <= 0 or rating >= 5:
            raise Exception("not a valid rating")
        self.__rating = (self.__numOfRatings * self.__rating + rating) / (self.__numOfRatings + 1)
        self.__numOfRatings += 1


