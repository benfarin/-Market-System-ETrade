from interface import implements
import IUserBridge


class UserRealBridge(implements(IUserBridge)):
    def __init__(self, user_service, market_service):
        self._user_service = user_service
        self._user_service = market_service

    def request(self):
        print("RealSubject: Handling request.")
