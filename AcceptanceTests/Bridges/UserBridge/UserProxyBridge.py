import zope
from AcceptanceTests.Bridges.UserBridge.IUserBridge import IUserBridge
from AcceptanceTests.Bridges.UserBridge import UserRealBridge

@zope.interface.implementer(IUserBridge)
class UserProxyBridge:
    def __init__(self, real_subject: UserRealBridge):
        self._real_subject = real_subject

    def request(self) -> bool:
        if self.check_access():
            self._real_subject.request()
        else:
            return True

    def check_access(self):
        return self._real_subject is None

    def register(self, username, password, phone, account_number, branch, country,
                 city, street, apartment_num, zip_code):
        if self.check_access():
            return True
        else:
            return self._real_subject.register(username, password, phone, account_number, branch, country,
                 city, street, apartment_num, zip_code)

    def login_guest(self):
        if self.check_access():
            return True
        else:
            return self._real_subject.login_guest()

    def login_member(self, oldUserId, user_name, password):
        if self.check_access():
            return True
        else:
            return self._real_subject.login_member(oldUserId, user_name, password)

    def add_product_to_cart(self, user_id, store_id, product_id, quantity):
        if self.check_access():
            return True
        return self._real_subject.add_product_to_cart(user_id, store_id, product_id, quantity)

    def purchaseProductWithoutAddress(self, userID, cardNumber, month, year, holderCardName, cvv, holderID,
                                   country, city, street, apartmentNum, zipCode):
        if self.check_access():
            return True
        return self._real_subject.purchaseProductWithoutAddress(userID, cardNumber, month, year, holderCardName, cvv, holderID,
                                                    country, city, street, apartmentNum, zipCode)

    def purchase_product(self, user_id, cardNumber, month, year, holderCardName, cvv, holderID):
        if self.check_access():
            return True
        return self._real_subject.purchase_product(user_id, cardNumber, month, year, holderCardName, cvv, holderID)

    def logout_member(self, userName):
        if self.check_access():
            return True
        else:
            return self._real_subject.logout_member(userName)

    def removeSystemManger_forTests(self, systemMangerName):
        if self.check_access():
            return True
        else:
            return self._real_subject.removeSystemManger_forTests(systemMangerName)

    def removeMember(self, systemManagerName, memberName):
        if self.check_access():
            return True
        else:
            return self._real_subject.removeMember(systemManagerName, memberName)

    def getAllActiveUsers(self, systemManagerName):
        if self.check_access():
            return True
        else:
            return self._real_subject.getAllActiveUsers(systemManagerName)

    def open_store(self, store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code):
        if self.check_access():
            return True
        return self._real_subject.open_store(store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code)

    def removeStore(self,store_id, user_id):
        if self.check_access():
            return True
        return self._real_subject.removeStore(store_id, user_id)

    def recreateStore(self,user_id, store_id):
        if self.check_access():
            return True
        return self._real_subject.recreateStore(user_id, store_id)

    def appoint_system_manager(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum, zipCode):
        if self.check_access():
            return True
        return self._real_subject.appoint_system_manager(userName, password, phone, accountNumber, brunch,
                                                         country, city, street, apartmentNum, zipCode)

    def enter_system(self):
        if self.check_access():
            return True
        return  self._real_subject.enter_system()

    def exit_system(self, guest_id):
        if self.check_access():
            return True
        return self._real_subject.exit_system(guest_id)

    def remove_prod_from_cart(self, user_id, store_id, prod_id):
        if self.check_access():
            return True
        return self._real_subject.remove_product_from_cart(user_id, store_id, prod_id)

    def update_prod_from_cart(self, user_id, store_id, prod_id, quantity):
        if self.check_access():
            return True
        return  self._real_subject.update_prod_from_cart(user_id, store_id, prod_id, quantity)

    def get_cart(self, user_id):
        if self.check_access():
            return True
        return self._real_subject.get_cart(user_id)

    def removeCart(self, userId):
        if self.check_access():
            return True
        return self._real_subject.removeCart(userId)

    def get_sum_after_discount(self, user_id):
        if self.check_access():
            return True
        return self._real_subject.get_sum_after_discount(user_id)

    def get_member_transaction(self, user_id):
        if self.check_access():
            return True
        return self._real_subject.get_member_transaction(user_id)

    def get_member_notifications(self, user_id):
        if self.check_access():
            return True
        return self._real_subject.get_member_notifications(user_id)

    def reset_management(self):
        if self.check_access():
            return True
        return self._real_subject.reset_management()

    def openNewBidOffer(self,userID,storeID,productID,newPrice):
        if self.check_access():
            return True
        return self._real_subject.openNewBidOffer(userID,storeID,productID,newPrice)

    def acceptBidOffer(self, userID, storeID, bID):
        if self.check_access():
            return True
        return self._real_subject.acceptBidOffer(userID, storeID, bID)

    def rejectOffer(self, userID, storeID, bID):
        if self.check_access():
            return True
        return self._real_subject.rejectOffer(userID, storeID, bID)

    def offerAlternatePrice(self, userID, storeID, bID, new_price):
        if self.check_access():
            return True
        return self._real_subject.offerAlternatePrice(userID, storeID, bID, new_price)

    def acceptOwnerAgreement(self, userId, storeID, ownerAcceptID):
        if self.check_access():
            return True
        return self._real_subject.acceptOwnerAgreement(userId, storeID, ownerAcceptID)

    def rejectOwnerAgreement(self, userId, storeID, ownerAcceptID):
        if self.check_access():
            return True
        return self._real_subject.rejectOwnerAgreement(userId, storeID, ownerAcceptID)

    def getBid(self, storeId, bid):
        if self.check_access():
            return True
        return self._real_subject.getBid(storeId, bid)

    def getAllStoreBids(self, storeId):
        if self.check_access():
            return True
        return self._real_subject.getAllStoreBids(storeId)

    def getOwnerAgreementById(self, storeId, oaId):
        if self.check_access():
            return True
        return self._real_subject.getOwnerAgreementById(storeId, oaId)

    def getAllStoreOwnerAgreements(self, storeId):
        if self.check_access():
            return True
        return self._real_subject.getAllStoreOwnerAgreements(storeId)



