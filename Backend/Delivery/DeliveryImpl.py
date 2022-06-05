import zope

from Backend.Delivery.DeliveryDetails import DeliveryDetails
from Backend.Delivery.DeliveryStatus import DeliveryStatus
from Backend.ExternalSystem.ExternalSystem import ExternalSystem
from Backend.Interfaces.IDelivery import IDelivery
from zope.interface import implements


@zope.interface.implementer(IDelivery)
class DeliveryImpl:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DeliveryImpl.__instance is None:
            DeliveryImpl()
        return DeliveryImpl.__instance

    def __init__(self):
        self.__deliverySystem: ExternalSystem = ExternalSystem.getInstance()
        if DeliveryImpl.__instance is None:
            DeliveryImpl.__instance = self

    def createDelivery(self, deliveryDetail: DeliveryDetails):  # (self, reciverID, phone, source, destination):
        try:
            address = deliveryDetail.getAddress().getStreet() + str(deliveryDetail.getAddress().getApartmentNum())
            params = {"action_type": "supply",
                      "name": deliveryDetail.getName(),
                      "address": address,
                      "city": deliveryDetail.getAddress().getCity(),
                      "country": deliveryDetail.getAddress().getCountry(),
                      "zip": str(deliveryDetail.getAddress().getZipCode())
                      }

            deliveryId = self.__deliverySystem.getInstance().CreateRequest(params)

            return DeliveryStatus(deliveryId, deliveryDetail.getUserID(), deliveryDetail.getStoreID(),
                                  "delivery succeeded")
        except Exception as e:
            return DeliveryStatus(-1, deliveryDetail.getUserID(), deliveryDetail.getStoreID(),
                                  "delivery failed")

    def cancelDelivery(self, deliveryStatus: DeliveryStatus):
        try:

            params = {"action_type": "cancel_supply",
                      "transaction_id": deliveryStatus.getDeliveryID(),
                      }

            self.__deliverySystem.getInstance().CancelRequest(params)
            deliveryStatus.setStatus("cancel delivery succeeded")
        except Exception as e:
            deliveryStatus.setStatus("cancel delivery failed")
