from Delivery.DeliverySystem import DeliverytSystem
from Delivery.DeliveryStatus import DeliveryStatus
from Delivery.DeliveryDetails import DeliveryDetails
from interfaces.IDelivery import IDelivery
from interface import implements


class Deliverylmpl(implements(IDelivery)):
    instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DeliverytSystem.__instance is None:
            Deliverylmpl()
        return Deliverylmpl.instance

    def __init__(self):
        self.__deliverySystem: DeliverytSystem = DeliverytSystem()
        self.__deliveryID = 0
        if Deliverylmpl.instance is None:
            Deliverylmpl.instance=self
    def createDelivery(self, deliveryDetail: DeliveryDetails):  #(self, reciverID, phone, source, destination):
        try:
            self.__deliverySystem.CreateDelivery(deliveryDetail.getUserId(),
                                               deliveryDetail.getPhone(),
                                               deliveryDetail.getSourceAdress(),
                                                deliveryDetail.getDestinationAdress())
            return DeliveryStatus(self.getDeliveryID(),deliveryDetail.getUserID(),deliveryDetail.getStoreID(),"delivery succeeded")
        except Exception:
            return DeliveryStatus(self.getDeliveryID(),deliveryDetail.getUserID(),deliveryDetail.getStoreID(),"delivery failed")



    def cancelDelivery(self, deliveryStatus: DeliveryStatus):
        try:
            self.__deliverySystem.CancelDelivery(deliveryStatus.getPackageID())
            DeliveryStatus.setStatus("cancel delivery succeeded")
        except Exception:
            DeliveryStatus.status("cancel delivery failed")

    def getDeliveryID(self):
        deliveryID = self.__deliveryID
        self.__deliveryID += 1
        return deliveryID
