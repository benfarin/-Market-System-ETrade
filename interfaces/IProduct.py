from interface import Interface


class IProduct(Interface):
    def setProductName(self, name):
        pass

    def setProductCategory(self, newCategory):
        pass