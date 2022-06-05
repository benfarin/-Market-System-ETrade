from zope.interface import Interface


class IDelivery(Interface):

    def createDelivery(self, deliveryDetail):
        pass

    def cancelDelivery(self, deliveryStatus):
        pass
