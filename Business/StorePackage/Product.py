class Product:

    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = price
        self.category = category  # String

    def getProductId(self):
        return self.id

    def getProductName(self):
        return self.name

    def getProductPrice(self):
        return self.price

    def getProductCategory(self):
        return self.category


