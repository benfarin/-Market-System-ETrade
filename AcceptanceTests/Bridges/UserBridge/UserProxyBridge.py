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

    def purchase_product(self, user_id, account_num, branch):
        if self.check_access():
            return True
        return self._real_subject.purchase_product(user_id, account_num, branch)

    def logout_member(self, user_id):
        if self.check_access():
            return True
        else:
            return self._real_subject.logout_member(user_id)

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

    def get_sum_after_discount(self, user_id):
        return self._real_subject.get_sum_after_discount(user_id)

    def get_member_transaction(self, user_id):
        return self._real_subject.get_member_transaction(user_id)


