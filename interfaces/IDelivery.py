from interface import Interface


class IDelivery(Interface):

    def createDelivery(self, deliveryStatus):
        pass

    def cancelDelivery(self, deliveryDetails):
        pass
