from ModelsBackend.models import StoreUserPermissionsModel


class StorePermission:
    def __init__(self, userId=None, model=None):
        if model is None:
            self.__model = StoreUserPermissionsModel.objects.get_or_create(userID=userId)[0]
            self.__userId = userId
            self.__stockManagement = False
            self.__appointManager = False
            self.__appointOwner = False
            self.__changePermission = False
            self.__closeStore = False
            self.__rolesInformation = False
            self.__purchaseHistoryInformation = False
            self.__discountPermission = False
            self.__bidPermission = False
        else:
            self.__model = model
            self.__userId = self.__model.userID.userid
            self.__stockManagement = self.__model.stockManagement
            self.__appointManager = self.__model.appointManager
            self.__appointOwner = self.__model.appointOwner
            self.__changePermission = self.__model.changePermission
            self.__closeStore = self.__model.closeStore
            self.__rolesInformation = self.__model.rolesInformation
            self.__purchaseHistoryInformation = self.__model.purchaseHistoryInformation
            self.__discountPermission = self.__model.discount
            self.__bidPermission = self.__model.bid


    def getUserId(self):
        return self.__userId

    def getModel(self):
        return self.__model

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
        return self.__discountPermission

    def hasPermission_Bid(self):
        return self.__bidPermission

    def setPermission_StockManagement(self, stockManagement):
        self.__stockManagement = stockManagement
        self.__model.stockManagement = stockManagement
        self.__model.save()

    def setPermission_AppointManager(self, appointManager):
        self.__appointManager = appointManager
        self.__model.appointManager = appointManager
        self.__model.save()

    def setPermission_AppointOwner(self, appointOwner):
        self.__appointOwner = appointOwner
        self.__model.appointOwner = appointOwner
        self.__model.save()

    def setPermission_ChangePermission(self, changePermission):
        self.__changePermission = changePermission
        self.__model.changePermission = changePermission
        self.__model.save()

    def setPermission_CloseStore(self, closeStore):
        self.__closeStore = closeStore
        self.__model.closeStore = closeStore
        self.__model.save()

    def setPermission_RolesInformation(self, rolesInformation):
        self.__rolesInformation = rolesInformation
        self.__model.rolesInformation = rolesInformation
        self.__model.save()

    def setPermission_PurchaseHistoryInformation(self, purchaseHistoryInformation):
        self.__purchaseHistoryInformation = purchaseHistoryInformation
        self.__model.purchaseHistoryInformation = purchaseHistoryInformation
        self.__model.save()

    def setPermission_Discount(self, discountPermission):
        self.__discountPermission = discountPermission
        self.__model.discount = discountPermission
        self.__model.save()

    def setPermission_Bid(self, bidPermission):
        self.__bidPermission = bidPermission
        self.__model.bid = bidPermission
        self.__model.save()

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