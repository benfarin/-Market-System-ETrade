import numpy as np


class DeliverytSystem:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DeliverytSystem.__instance is None:
            DeliverytSystem()
        return DeliverytSystem.__instance

    def __init__(self):
        if DeliverytSystem.__instance is None:
            DeliverytSystem.__instance = self

    def CreateDelivery(self, reciverID, phone, source, destination):
        if np.random.random() < 0.25:
            raise Exception("Delivery failed")
        return True

    def CancelDelivery(self, derliveryID):
        if derliveryID >= 0:
            return True
        else:
            raise Exception("illegal DeliveryID")
