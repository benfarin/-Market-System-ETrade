class StorePermission:
    def __init__(self, userId):
        self.__userId = userId
        self.__stockManagement = False
        self.__appointManager = False
        self.__appointOwner = False
        self.__changePermission = False
        self.__closeStore = False
        self.__rolesInformation = False
        self.__purchaseHistoryInformation = False

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

    def printPermission(self):
        permission = ""
        if self.__stockManagement:
            permission += "\n\tstock management"
        if self.__appointManager:
            permission += "\n\tappoint manager"
        if self.__appointOwner:
            permission += "\n\tappoint owner"
        if self.__changePermission:
            permission += "\n\tchange permission"
        if self.__closeStore:
            permission += "\n\tclose store"
        if self.__rolesInformation:
            permission += "\n\troles information"
        if self.__purchaseHistoryInformation:
            permission += "\n\tpurchase history information"
        return permission

    def hasPermissions(self):
        return self.__stockManagement is not False and self.__appointManager is not False and \
               self.__appointOwner is not False and self.__changePermission is not False and \
               self.__closeStore is not False and self.__rolesInformation is not False and \
               self.__purchaseHistoryInformation is not False