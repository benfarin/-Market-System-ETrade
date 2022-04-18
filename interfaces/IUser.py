from interface import implements, Interface
class IUser(Interface):

   def getCart(self, name):
      pass

   def editCart(self,store, product, quantity): # update products in the cart/
      pass

   def saveProduct(self,store, product, quantity): # add product
      pass

   def getProducts(self,name): # add product
      pass

   def getHistory(self,name):
      pass

   def get_Products_from_stores(self): # get all the products from all the stores
      pass

   def search_Product(self): # talk with kfirrrrrrrrrrr
      pass

   def purchase_Product(self, bankAccount, phone, address ): # bank - is bank object , address - object of address
      pass

   def getShoppingCart(self):
      pass