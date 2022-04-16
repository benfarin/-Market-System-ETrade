from interface import implements
import IUserBridge
from AcceptanceTests.Bridges.UserBridge import UserRealBridge


class UserProxyBridge(implements(IUserBridge)):
    def __init__(self, real_subject: UserRealBridge):
        self._real_subject = real_subject

    def request(self) -> bool:
        if self.check_access():
            self._real_subject.request()
        else:
            return True

    def check_access(self):
        return self._real_subject is None

    def register(self, username, password, confirm_pass, email):
        if self.check_access():
            return True
        else:
            return self._real_subject.register(username, password, confirm_pass, email)

    def login(self, username, password):
        if self.check_access():
            return True
        else:
            return self._real_subject.login(username, password)

