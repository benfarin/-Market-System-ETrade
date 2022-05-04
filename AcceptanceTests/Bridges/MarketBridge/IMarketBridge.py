from zope.interface import Interface


class IMarketBridge(Interface):
    def request(self):
        pass
