from Business.StorePackage.StorePermission import StorePermission


class StorePermissionDTO:
    def __init__(self, storePermission: StorePermission):
        self.__userId = storePermission.getUserId()
        self.__stockManagement = storePermission.hasPermission_StockManagement()
        self.__appointManager = storePermission.hasPermission_AppointManager()
        self.__appointOwner = storePermission.hasPermission_AppointOwner()
        self.__changePermission = storePermission.hasPermission_ChangePermission()
        self.__closeStore = storePermission.hasPermission_CloseStore()
        self.__rolesInformation = storePermission.hasPermission_RolesInformation()
        self.__purchaseHistoryInformation = storePermission.hasPermission_PurchaseHistoryInformation()
        self.__discountPermissions = storePermission.hasPermission_Discount()

    def getUserId(self):
        return self.__userId

    def hasPermission_StockManagement(self):
        return self.__stockManagement

    def hasPermission_AppointManager(self):
        return self.__appointManager

    def hasPermission_AppointOwner(self):
        return self.__appointOwner

    def hasPermission_ChangePermission(self):
        return self.__changePermission

    def hasPermission_CloseStore(self):
        return self.__closeStore

    def hasPermission_RolesInformation(self):
        return self.__rolesInformation

    def hasPermission_PurchaseHistoryInformation(self):
        return self.__purchaseHistoryInformation

    def hasPermission_Discount(self):
        return self.__discountPermissions

    def setPermission_StockManagement(self, stockManagement):
        self.__stockManagement = stockManagement

    def setPermission_AppointManager(self, appointManager):
        self.__appointManager = appointManager

    def setPermission_AppointOwner(self, appointOwner):
        self.__appointOwner = appointOwner

    def setPermission_ChangePermission(self, changePermission):
        self.__changePermission = changePermission

    def setPermission_CloseStore(self, closeStore):
        self.__closeStore = closeStore

    def setPermission_RolesInformation(self, rolesInformation):
        self.__rolesInformation = rolesInformation

    def setPermission_PurchaseHistoryInformation(self, purchaseHistoryInformation):
        self.__purchaseHistoryInformation = purchaseHistoryInformation

    def setPermission_Discount(self, discountPermissions):
        self.__discountPermissions = discountPermissions

    def __str__(self):
        toReturn = "permissions for user: " + str(self.__userId) + ":"
        toReturn += "\n\t\t\tstock permission: " + str(self.__stockManagement)
        toReturn += "\n\t\t\tappoint manager: " + str(self.__appointManager)
        toReturn += "\n\t\t\tappoint owner: " + str(self.__appointOwner)
        toReturn += "\n\t\t\tclose store: " + str(self.__closeStore)
        toReturn += "\n\t\t\tget role information: " + str(self.__rolesInformation)
        toReturn += "\n\t\t\tget purchase history information: " + str(self.__purchaseHistoryInformation)
        return toReturn + "\n\t\t\tdiscount permission: " + str(self.__discountPermissions)