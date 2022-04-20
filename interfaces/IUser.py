from interface import implements, Interface
class IUser(Interface):
   def guestLogin(self):
      pass
   def guestLogOut(self, guestID):
       pass

   def memberSignUp(self, userName, password, phone, address, bank, icart):
      pass

   def memberLogin(self, userID, password):
      pass

   def logoutMember(self, userID):
      pass

   def checkPassword(self, userID, password):
      pass

   def checkAssigners(self, assignerID, assigneID):
      pass

   def saveProducts(self, assignerID, store):
      pass

   def appointManagerToStore(self, storeID, assignerID, assigneID):
      pass

   def appointOwnerToStore(self, storeID, assignerID, assigneID):
      pass

   def setStockManagementPermission(self, storeID, assignerID, assigneID):
      pass

   def setAppointManagerPermission(self, storeID, assignerID, assigneID):
      pass

   def setAppointOwnerPermission(self, storeID, assignerID, assigneID):
      pass

   def setChangePermission(self, storeID, assignerID, assigneID):
      pass

   def setRolesInformationPermission(self, storeID, assignerID, assigneID):
      pass

   def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneID):
      pass
