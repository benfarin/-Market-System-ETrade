class StorePermission:
    def __init__(self):
        self.__stockManagement = False
        self.__appointManager = False
        self.__appointOwner = False
        self.__changePermission = False
        self.__closeStore = False
        self.__rolesInformation = False
        self.__purchaseHistoryInformation = False

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
