from zope.interface import Interface


class IUserBridge(Interface):
    def request(self):
        pass
