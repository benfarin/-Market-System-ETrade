from ModelsBackend.models import StoreUserPermissionsModel


class StorePermission:
    def __init__(self, userId=None, model=None):
        # self.__userId = userId
        # self.__stockManagement = False
        # self.__appointManager = False
        # self.__appointOwner = False
        # self.__changePermission = False
        # self.__closeStore = False
        # self.__rolesInformation = False
        # self.__purchaseHistoryInformation = False
        # self.__discountPermission = False
        if model is None:
            self.__model = StoreUserPermissionsModel.objects.get_or_create(userID=userId)[0]
        else:
            self.__model = model

    def getUserId(self):
        return self.__model.userID.userid

    def hasPermission_StockManagement(self):
        return self.__model.stockManagement

    def hasPermission_AppointManager(self):
        return self.__model.appointManager

    def hasPermission_AppointOwner(self):
        return self.__model.appointOwner

    def hasPermission_ChangePermission(self):
        return self.__model.changePermission

    def hasPermission_CloseStore(self):
        return self.__model.closeStore

    def hasPermission_RolesInformation(self):
        return self.__model.rolesInformation

    def hasPermission_PurchaseHistoryInformation(self):
        return self.__model.purchaseHistoryInformation

    def hasPermission_Discount(self):
        return self.__model.discount

    def setPermission_StockManagement(self, stockManagement):
        self.__model.stockManagement = stockManagement

    def setPermission_AppointManager(self, appointManager):
        self.__model.appointManager = appointManager

    def setPermission_AppointOwner(self, appointOwner):
        self.__model.appointOwner = appointOwner

    def setPermission_ChangePermission(self, changePermission):
        self.__model.changePermission = changePermission

    def setPermission_CloseStore(self, closeStore):
        self.__model.closeStore = closeStore

    def setPermission_RolesInformation(self, rolesInformation):
        self.__model.rolesInformation = rolesInformation

    def setPermission_PurchaseHistoryInformation(self, purchaseHistoryInformation):
        self.__model.purchaseHistoryInformation = purchaseHistoryInformation

    def setPermission_Discount(self, discountPermission):
        self.__model.discount = discountPermission

    def printPermission(self):
        permission = ""
        if self.__model.stockManagement:
            permission += "\n\tstock management"
        if self.__model.appointManager:
            permission += "\n\tappoint manager"
        if self.__model.appointOwner:
            permission += "\n\tappoint owner"
        if self.__model.changePermission:
            permission += "\n\tchange permission"
        if self.__model.closeStore:
            permission += "\n\tclose store"
        if self.__model.rolesInformation:
            permission += "\n\troles information"
        if self.__model.purchaseHistoryInformation:
            permission += "\n\tpurchase history information"
        return permission