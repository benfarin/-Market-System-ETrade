from interface import Interface

from Delivery.DeliveryDetails import DeliveryDetails
from Delivery.DeliveryStatus import DeliveryStatus


class IDelivery(Interface):

    def createDelivery(self, deliveryDetail: DeliveryDetails):
        pass

    def cancelDelivery(self, deliveryStatus: DeliveryStatus):
        pass
