from typing import List


class Product:

    def __init__(self, Id, name, price, category, keyword):
        self.__id = Id
        self.__name = name
        self.__price = price
        self.__category = category  # String
<<<<<<< HEAD
        self.__keyword : Dict[str,int] = keyword   #the value is integer , may use as a priority at next

    def removeKeyWord(self,keyword):
        if self.__keyword.get(storeId) is not None:
            self.__bags.pop(storeId)
            return True
        else:
            return False
    def isExistKeyword(self,keyword): # return true if the product include the keyword as parameter
        if self.__keyword.get(keyword) is not None:
            return True
        else:
            return False

    def addKeyWord(self,keyword): #when adding keyword it get it's default value 1
        if self.__keyword.get(storeId) is None:
            self.__keyword[keyword] = 1
            return  True
        return  False


=======
        self.__keywords: List = keyword
>>>>>>> 467c252b2ec8b4dd444758cfe108d5883b34efab

    def getProductId(self):
        return self.__id

    def getProductName(self):
        return self.__name

    def getProductPrice(self):
        return self.__price

    def getProductCategory(self):
        return self.__category

    def setProductName(self, name):
        self.__name = name

    def setProductPrice(self, price):
        self.__price = price

    def setProductCategory(self, category):
        self.__category = category

    def addKeyWord(self, keyword):
        if keyword not in self.__keywords:
            self.__keywords.append(keyword)

    def removeKeyWord(self, keyword):
        if keyword not in self.__keywords:
            raise Exception("cannot remove keyword that doesn't exists")
        self.__keywords.remove(keyword)

    def isExistsKeyword(self, keyword):
        return keyword in self.__keywords

    def printForEvents(self):
        productStr = "\n\t\t\tid: " + str(self.__id)
        productStr += "\n\t\t\tname: " + self.__name
        productStr += "\n\t\t\tprice: " + str(self.__price)
        productStr += "\n\t\t\tcategory: " + self.__category
        productStr += "\n\t\t\tkeywords: "
        for keyword in self.__keywords:
            productStr += "\n\t\t\t\t" + keyword
        return productStr

